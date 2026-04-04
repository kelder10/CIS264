import json
from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q

from .models import Reservation, Waiver, PromoCode
from .forms import ReservationForm, WaiverForm, PromoCodeForm, ReservationCancelForm
from bikes.models import Bike
from payments.models import Payment
from locations.models import Location


def check_availability(request):
    """AJAX endpoint to check bike availability for dates."""
    bike_id = request.GET.get('bike_id')
    date_str = request.GET.get('date')

    if not bike_id or not date_str:
        return JsonResponse({'error': 'Bike ID and date are required'}, status=400)

    try:
        bike = Bike.objects.get(id=bike_id)
        from datetime import datetime
        check_date = datetime.strptime(date_str, '%Y-%m-%d').date()

        available = bike.is_available_for_date(check_date)
        quantity = bike.get_available_quantity(check_date)

        return JsonResponse({
            'available': available,
            'quantity': quantity,
            'bike_name': bike.name
        })
    except Bike.DoesNotExist:
        return JsonResponse({'error': 'Bike not found'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)


@login_required
def create_reservation(request, bike_slug):
    """Create a new reservation and digitally station the bike at the dock."""
    bike = get_object_or_404(Bike, slug=bike_slug, is_available=True)

    if bike.is_maintenance:
        messages.error(request, 'This bike is currently under maintenance.')
        return redirect('bike_detail', slug=bike_slug)

  
    active_bookings = Reservation.objects.filter(
        bike=bike,
        status__in=['pending', 'confirmed', 'paid', 'active']
    ).exclude(status='cancelled')

    booked_dates = []
    for booking in active_bookings:
        current_date = booking.rental_date
        while current_date <= booking.return_date:
            booked_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
    
    booked_dates_json = json.dumps(booked_dates)

    if request.method == 'POST':
        location_id = request.POST.get('pickup_location')
        
        if not location_id:
            messages.error(request, "Please select a Smart-Dock location.")
            form = ReservationForm(request.POST, bike=bike)
            return render(request, 'reservations/create_reservation.html', {
                'form': form, 'bike': bike, 'booked_dates_json': booked_dates_json
            })

        location = get_object_or_404(Location, id=location_id)
        
        if location.is_full:
            messages.error(request, f"{location.name} is currently at capacity.")
            form = ReservationForm(request.POST, bike=bike)
            return render(request, 'reservations/create_reservation.html', {
                'form': form, 'bike': bike, 'booked_dates_json': booked_dates_json
            })

        form = ReservationForm(request.POST, bike=bike)
        if form.is_valid():
            try:
                with transaction.atomic():
                    reservation = form.save(commit=False)
                    reservation.user = request.user
                    reservation.bike = bike
                    reservation.pickup_location = location 
                    
                    # --- DURATION LOGIC ---
                    rental_date = form.cleaned_data['rental_date']
                    return_date = form.cleaned_data['return_date']
                    
                    if reservation.rental_type == 'hourly':
                        reservation.rental_duration = 4 
                    else:
                        days = (return_date - rental_date).days + 1
                        reservation.rental_duration = max(1, days)

                    reservation.save()
                    
                    # --- ACCESSORY LOGIC ---
                    selected_accessories = form.cleaned_data.get('accessories')
                    if selected_accessories:
                        for accessory in selected_accessories:
                         
                            reservation.reservation_accessories.create(
                                accessory=accessory,
                                price_at_time=accessory.price_per_day
                            )
                    
                    reservation.calculate_prices()
                    reservation.save()
                    
                    # --- SMART-DOCK LOGIC ---
                    # Assign the bike to the location
                    bike.location = location
                    bike.save()

                    # Update the Location counter
                    location.current_bikes = location.bikes.count()
                    location.save()
                    
                    messages.success(request, f'Reservation created for {bike.name}. It is waiting at {location.name}.')
                    return redirect('waiver', reservation_id=reservation.id)
                    
                    messages.success(request, f'Reservation created for {bike.name}. It is waiting at {location.name}.')
                    return redirect('waiver', reservation_id=reservation.id)
                
            except Exception as e:
                messages.error(request, f"System error: {e}")
        else:
            print(form.errors)

    else:
        initial = {}
        if 'date' in request.GET:
            initial['rental_date'] = request.GET.get('date')
            initial['return_date'] = request.GET.get('date')
        form = ReservationForm(bike=bike, initial=initial)

    context = {
        'form': form,
        'bike': bike,
        'booked_dates_json': booked_dates_json, 
    }
    return render(request, 'reservations/create_reservation.html', context)


@login_required
def waiver(request, reservation_id):
    """Waiver signing view."""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    if reservation.waiver_signed:
        messages.info(request, 'Waiver already signed. Proceeding to payment.')
        return redirect('payment', reservation_id=reservation.id)

    if request.method == 'POST':
        form = WaiverForm(request.POST)
        if form.is_valid():
            waiver_obj = form.save(commit=False)
            waiver_obj.user = request.user
            waiver_obj.reservation = reservation
            waiver_obj.save()

            # Update reservation status
            reservation.waiver_signed = True
            reservation.waiver_signed_at = timezone.now()
            reservation.save()

            messages.success(request, 'Waiver signed. Please proceed to payment.')
            return redirect('payment', reservation_id=reservation.id)
    else:
        # Pre-fill with User profile data
        initial = {
            'full_name': request.user.get_full_name(),
            'signature': request.user.get_full_name(),
            'emergency_contact_name': getattr(request.user, 'emergency_contact_name', ''),
            'emergency_contact_phone': getattr(request.user, 'emergency_contact_phone', ''),
        }
        form = WaiverForm(initial=initial)

    return render(request, 'reservations/waiver.html', {
        'form': form,
        'reservation': reservation,
        'bike': reservation.bike,
    })

@login_required
def reservation_detail(request, pk):
    """View reservation details."""
    reservation = get_object_or_404(
        Reservation.objects.select_related('bike', 'user'),
        pk=pk,
        user=request.user
    )

    context = {
        'reservation': reservation,
        'accessories': reservation.reservation_accessories.select_related('accessory').all(),
    }
    return render(request, 'reservations/reservation_detail.html', context)


@login_required
def my_reservations(request):
    """List all user reservations."""
    reservations = Reservation.objects.filter(
        user=request.user
    ).select_related('bike').order_by('-created_at')

    context = {
        'reservations': reservations,
    }
    return render(request, 'reservations/my_reservations.html', context)


@login_required
def cancel_reservation(request, pk):
    """Cancel a reservation."""
    reservation = get_object_or_404(
        Reservation,
        pk=pk,
        user=request.user
    )

    # Check if reservation can be cancelled
    if reservation.status in ['completed', 'cancelled']:
        messages.error(request, 'This reservation cannot be cancelled.')
        return redirect('reservation_detail', pk=pk)

    if request.method == 'POST':
        form = ReservationCancelForm(request.POST)
        if form.is_valid():
            reservation.status = 'cancelled'
            reservation.admin_notes = form.cleaned_data.get('reason', '')
            reservation.save()

            messages.success(request, 'Your reservation has been cancelled.')
            return redirect('my_reservations')
    else:
        form = ReservationCancelForm()

    context = {
        'form': form,
        'reservation': reservation,
    }
    return render(request, 'reservations/cancel_reservation.html', context)


@login_required
def reservation_confirmation(request, pk):
    """Reservation confirmation page after payment."""
    reservation = get_object_or_404(
        Reservation.objects.select_related('bike', 'user'),
        pk=pk,
        user=request.user
    )

    # Get payment info
    try:
        payment = Payment.objects.get(reservation=reservation)
    except Payment.DoesNotExist:
        payment = None

    context = {
        'reservation': reservation,
        'payment': payment,
        'accessories': reservation.reservation_accessories.select_related('accessory').all(),
    }
    return render(request, 'reservations/reservation_confirmation.html', context)


def unlock_bike(request, pk):
    new_res_id = request.GET.get('res_id')
    if new_res_id:
        return redirect('reservations:unlock_bike', pk=new_res_id)

    # Get the specific reservation
    reservation = get_object_or_404(Reservation, id=pk)
    
    # Identify the current location
    location = reservation.pickup_location
    if not location:
        location = Location.objects.all().first()

    # Calculate "Your Current Dock" stats
    current_bikes = Bike.objects.filter(location=location, is_available=True).count()
    slots = getattr(location, 'total_slots', 10) 
    percent_full = int((current_bikes / max(1, slots)) * 100)
    
    # Prepare "Other Network Locations"
    all_locations = Location.objects.all()
    for loc in all_locations:
        loc_bike_count = Bike.objects.filter(location=loc, is_available=True).count()
        loc_total = getattr(loc, 'total_slots', 10)
        loc.percent = int((loc_bike_count / max(1, loc_total)) * 100)
    
    context = {
        'location': location,
        'reservation': reservation,
        'all_locations': all_locations,
        'current_bikes': current_bikes,
        'percent_full': percent_full,
        'available_slots': slots - current_bikes,
    }
    
    return render(request, 'reservations/unlock_interface.html', context)

def process_unlock(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    bike = reservation.bike
    
    # Update status
    bike.status = 'in_use'
    
    # CLEAR the location 
    bike.location = None 
    bike.save()
    
    reservation.status = 'active'
    reservation.save()
    

    return redirect('unlock_bike', pk=reservation.id)

def process_return(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    bike = reservation.bike
    
    return_location = reservation.pickup_location 
    
    bike.status = 'available'
    bike.location = return_location 
    bike.is_available = True  
    bike.save()
    
    reservation.status = 'completed'
    reservation.save()
    
    messages.success(request, f"Return Successful! {bike.name} is locked at {return_location.name}.")
    return redirect('unlock_bike', pk=reservation_id)

def find_next_reservation(request):
    res_id = request.GET.get('res_id')
    if res_id:
        try:
            next_res = Reservation.objects.get(id=res_id, user=request.user)
           
            today = timezone.localtime(timezone.now()).date()
            yesterday = today - timedelta(days=1)
            
            if next_res.rental_date < yesterday:
                messages.error(request, f"Res #{res_id} was scheduled for {next_res.rental_date}, which has passed.")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            
            if next_res.rental_date > today:
                 messages.error(request, f"Res #{res_id} is scheduled for {next_res.rental_date}. Please come back then!")
                 return redirect(request.META.get('HTTP_REFERER', '/'))

            return redirect('unlock_bike', pk=next_res.id)
            
        except Reservation.DoesNotExist:
            messages.error(request, "Reservation not found or belongs to another account.")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


def confirm_pickup_location(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    if request.method == "POST":
        location_id = request.POST.get('location_id')
        selected_location = get_object_or_404(Location, id=location_id)
        
        with transaction.atomic():
            reservation.pickup_location = selected_location
            reservation.save()
            
            bike = reservation.bike
            bike.location = selected_location
            bike.status = 'available' 
            bike.is_available = True 
            bike.save()
        
        return redirect('reservation_detail', pk=reservation.id)