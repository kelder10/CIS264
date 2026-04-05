import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from bikes.models import Bike, BikeCategory
from reviews.models import Review
from .models import Trail
from .forms import ContactForm, WeatherZipForm

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model

from reservations.models import Reservation
from payments.models import Payment

def home(request):
    """Homepage view with featured content."""
    # Get featured bikes (available bikes, limited to 6)
    featured_bikes = Bike.objects.filter(
        is_available=True,
        is_maintenance=False
    ).select_related('category')[:6]
    
    # Get featured reviews for carousel
    featured_reviews = Review.objects.filter(
        is_approved=True,
        is_featured=True
    ).select_related('user')[:6]
    
    # Get featured trails
    featured_trails = Trail.objects.filter(is_featured=True)[:3]
    
    # Get bike categories
    categories = BikeCategory.objects.all()
    
    # Get bike counts by category
    adult_count = Bike.objects.filter(category__slug='adult-bikes', is_available=True).count()
    kids_count = Bike.objects.filter(category__slug='kids-bikes', is_available=True).count()
    mountain_count = Bike.objects.filter(category__slug='mountain-bikes', is_available=True).count()
    tandem_count = Bike.objects.filter(category__slug='tandem-bikes', is_available=True).count()
    
    # Weather form
    weather_form = WeatherZipForm()
    
    context = {
        'featured_bikes': featured_bikes,
        'featured_reviews': featured_reviews,
        'featured_trails': featured_trails,
        'categories': categories,
        'weather_form': weather_form,
        'adult_count': adult_count,
        'kids_count': kids_count,
        'mountain_count': mountain_count,
        'tandem_count': tandem_count,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page view."""
    return render(request, 'core/about.html')


def trails(request):
    """Trails listing page."""
    all_trails = Trail.objects.all()
    
    # Filter by difficulty if provided
    difficulty = request.GET.get('difficulty')
    if difficulty:
        all_trails = all_trails.filter(difficulty=difficulty)
    
    context = {
        'trails': all_trails,
        'difficulty_choices': Trail.DIFFICULTY_LEVELS,
        'selected_difficulty': difficulty,
    }
    return render(request, 'core/trails.html', context)


def contact(request):
    """Contact page with form."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Thank you for your inquiry! We will get back to you within 24 hours.'
            )
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'core/contact.html', context)


@require_http_methods(['GET'])
def weather_api(request):
    """API endpoint to fetch weather data by ZIP code."""
    zip_code = request.GET.get('zip_code', '')
    
    if not zip_code:
        return JsonResponse({'error': 'ZIP code is required'}, status=400)
    
    api_key = settings.OPENWEATHER_API_KEY
    
    # If no API key is configured, return mock data for demo
    if not api_key:
        # Return mock weather data for demonstration
        return JsonResponse({
            'location': f'Indian Creek Area ({zip_code})',
            'temperature': 72,
            'feels_like': 74,
            'condition': 'Partly Cloudy',
            'description': 'Great conditions for biking!',
            'humidity': 65,
            'wind_speed': 8,
            'icon': '02d',
            'forecast_url': f'https://weather.com/weather/today/l/{zip_code}',
            'mock': True
        })
    
    try:
        # Call OpenWeather API
        url = f'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'zip': f'{zip_code},us',
            'appid': api_key,
            'units': 'imperial'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if response.status_code != 200:
            return JsonResponse(
                {'error': data.get('message', 'Failed to fetch weather data')},
                status=response.status_code
            )
        
        # Format weather data
        weather_data = {
            'location': data['name'],
            'temperature': round(data['main']['temp']),
            'feels_like': round(data['main']['feels_like']),
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'].title(),
            'humidity': data['main']['humidity'],
            'wind_speed': round(data['wind']['speed']),
            'icon': data['weather'][0]['icon'],
            'forecast_url': f'https://weather.com/weather/today/l/{zip_code}',
        }
        
        return JsonResponse(weather_data)
        
    except requests.RequestException as e:
        return JsonResponse(
            {'error': f'Failed to fetch weather data: {str(e)}'},
            status=500
        )


def handler404(request, exception):
    """Custom 404 handler."""
    return render(request, 'core/404.html', status=404)


def handler500(request):
    """Custom 500 handler."""
    return render(request, 'core/500.html', status=500)


######admin dashboard


User = get_user_model()


@staff_member_required
def admin_dashboard(request):
    recent_reservations = Reservation.objects.select_related("user", "bike").order_by("-created_at")[:8]
    total_reservations = Reservation.objects.count()
    active_reservations = Reservation.objects.filter(
    status__in=["pending", "confirmed", "paid"]
).count()

    total_bikes = Bike.objects.count()
    available_bikes = Bike.objects.filter(
    is_available=True,
    is_maintenance=False
).count()
    maintenance_bikes = Bike.objects.filter(
    is_maintenance=True
).count()
    
    total_payments = Payment.objects.count()
    completed_payments = Payment.objects.filter(status__iexact="completed").count()

    total_reviews = Review.objects.count()
    pending_reviews = Review.objects.filter(is_approved=False).count()
    latest_reviews = Review.objects.select_related("user").order_by("-created_at")[:5]

    signed_waivers = Reservation.objects.filter(waiver_signed=True).count()
    staff_count = User.objects.filter(is_staff=True).count()

    context = {
        "total_bikes": total_bikes,
        "available_bikes": available_bikes,
        "maintenance_bikes": maintenance_bikes,
        "total_reservations": total_reservations,
        "active_reservations": active_reservations,
        "total_payments": total_payments,
        "completed_payments": completed_payments,
        "total_reviews": total_reviews,
        "pending_reviews": pending_reviews,
        "recent_reservations": recent_reservations,
        "latest_reviews": latest_reviews,
        "signed_waivers": signed_waivers,
        "staff_count": staff_count,
    }

    return render(request, "admin_dashboard/admin.html", context)

User = get_user_model()

##added for ability to adjust in admin dashboard

@staff_member_required
def admin_bikes(request):
    bikes = Bike.objects.select_related("category", "size").order_by("name")
    return render(request, "admin_dashboard/admin_bikes.html", {"bikes": bikes})


@staff_member_required
def toggle_bike_availability(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    bike.is_available = not bike.is_available
    if not bike.is_available:
        bike.is_maintenance = False
    bike.save()

    messages.success(request, f"{bike.name} availability updated.")
    return redirect("admin_bikes")


@staff_member_required
def toggle_bike_maintenance(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    bike.is_maintenance = not bike.is_maintenance
    if bike.is_maintenance:
        bike.is_available = False
    bike.save()

    messages.success(request, f"{bike.name} maintenance status updated.")
    return redirect("admin_bikes")


@staff_member_required
def admin_reservations(request):
    reservations = Reservation.objects.select_related("user", "bike").order_by("-created_at")
    return render(request, "admin_dashboard/admin_reservations.html", {"reservations": reservations})


@staff_member_required
def update_reservation_status(request, reservation_id, new_status):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    allowed_statuses = ["pending", "confirmed", "paid", "completed", "cancelled"]
    if new_status in allowed_statuses:
        reservation.status = new_status
        reservation.save()
        messages.success(request, f"Reservation #{reservation.id} updated to {new_status}.")
    else:
        messages.error(request, "Invalid reservation status.")

    return redirect("admin_reservations")


@staff_member_required
def admin_reviews(request):
    reviews = Review.objects.select_related("user", "bike").order_by("-created_at")
    return render(request, "admin_dashboard/admin_reviews.html", {"reviews": reviews})


@staff_member_required
def approve_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = True
    review.save()
    messages.success(request, f"Review #{review.id} approved.")
    return redirect("admin_reviews")


@staff_member_required
def unapprove_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.is_approved = False
    review.save()
    messages.success(request, f"Review #{review.id} marked unapproved.")
    return redirect("admin_reviews")


@staff_member_required
def admin_payments(request):
    payments = Payment.objects.select_related("reservation", "reservation__user", "reservation__bike").order_by("-created_at")
    return render(request, "admin_dashboard/admin_payments.html", {"payments": payments})

@staff_member_required
def refund_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if payment.status == "completed":
        payment.status = "refunded"
        payment.save()
        messages.success(request, f"Payment #{payment.id} marked as refunded.")
    else:
        messages.error(request, f"Only completed payments can be refunded. Current status: {payment.status}")

    return redirect("admin_payments")


@staff_member_required
def void_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if payment.status in ["pending", "processing"]:
        payment.status = "failed"
        payment.save()
        messages.success(request, f"Payment #{payment.id} was voided.")
    else:
        messages.error(request, f"Only pending or processing payments can be voided. Current status: {payment.status}")

    return redirect("admin_payments")
