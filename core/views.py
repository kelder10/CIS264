import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from bikes.models import Bike, BikeCategory
from reviews.models import Review
from .models import Trail
from .forms import ContactForm, WeatherZipForm


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
