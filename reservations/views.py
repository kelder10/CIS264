from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from bikes.models import Bike
from payments.models import Payment
from .models import Reservation, Waiver, PromoCode
from .forms import ReservationForm, WaiverForm, PromoCodeForm, ReservationCancelForm


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
    """Create a new reservation."""
    bike = get_object_or_404(Bike, slug=bike_slug, is_available=True)

    if bike.is_maintenance:
        messages.error(request, 'This bike is currently under maintenance.')
        return redirect('bike_detail', slug=bike_slug)

    if request.method == 'POST':
        form = ReservationForm(request.POST, bike=bike)
        if form.is_valid():
            with transaction.atomic():
                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.bike = bike
                reservation.rental_type = form.cleaned_data.get('rental_type', 'daily')

                # Calculate rental duration
                rental_date = form.cleaned_data['rental_date']
                return_date = form.cleaned_data['return_date']

                if reservation.rental_type == 'hourly':
                    # For hourly, default to 4 hours if not specified
                    reservation.rental_duration = 4
                else:
                    reservation.rental_duration = (return_date - rental_date).days + 1

                # Calculate initial prices before first save
                # This is safe now because calculate_prices() checks whether self.pk exists
                reservation.calculate_prices()
                reservation.save()

                # Add accessories after reservation has a primary key
                accessories = form.cleaned_data.get('accessories', [])
                for accessory in accessories:
                    from .models import ReservationAccessory
                    ReservationAccessory.objects.create(
                        reservation=reservation,
                        accessory=accessory,
                        quantity=1,
                        price_at_time=accessory.price_per_day or accessory.price
                    )

                # Recalculate with accessories included
                reservation.calculate_prices()
                reservation.save()

                messages.success(
                    request,
                    f'Reservation created for {bike.name}. Please complete the waiver to continue.'
                )
                return redirect('waiver', reservation_id=reservation.id)
    else:
        # Pre-populate dates if provided
        initial = {}
        if 'date' in request.GET:
            initial['rental_date'] = request.GET.get('date')
            initial['return_date'] = request.GET.get('date')
        form = ReservationForm(bike=bike, initial=initial)

    context = {
        'form': form,
        'bike': bike,
    }
    return render(request, 'reservations/create_reservation.html', context)


@login_required
def waiver(request, reservation_id):
    """Waiver signing view."""
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        user=request.user
    )

    # Check if waiver already signed
    if reservation.waiver_signed:
        messages.info(request, 'Waiver already signed. Proceeding to payment.')
        return redirect('payment', reservation_id=reservation.id)

    if request.method == 'POST':
        form = WaiverForm(request.POST)
        if form.is_valid():
            waiver = form.save(commit=False)
            waiver.user = request.user
            waiver.reservation = reservation
            waiver.save()

            # Update reservation
            reservation.waiver_signed = True
            reservation.waiver_signed_at = timezone.now()
            reservation.save()

            messages.success(request, 'Waiver signed successfully. Please proceed to payment.')
            return redirect('payment', reservation_id=reservation.id)
    else:
        # Pre-fill with user info
        initial = {
            'full_name': request.user.get_full_name(),
            'signature': request.user.get_full_name(),
            'emergency_contact_name': request.user.emergency_contact_name,
            'emergency_contact_phone': request.user.emergency_contact_phone,
        }
        form = WaiverForm(initial=initial)

    context = {
        'form': form,
        'reservation': reservation,
        'bike': reservation.bike,
    }
    return render(request, 'reservations/waiver.html', context)


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