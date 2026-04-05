from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Bike, BikeCategory, BikeSize, Accessory


def bike_list(request):
    """List all available bikes."""
    bikes = Bike.objects.filter(
        is_available=True, 
        is_maintenance=False
    ).select_related('category', 'size')
    
    category_slug = request.GET.get('category')
    if category_slug:
        bikes = bikes.filter(category__slug=category_slug)
    
    bike_type = request.GET.get('type')
    if bike_type:
        bikes = bikes.filter(bike_type=bike_type)
    
    size = request.GET.get('size')
    if size:
        bikes = bikes.filter(size__size_inches=size)
    
    search = request.GET.get('search')
    if search:
        bikes = bikes.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(features__icontains=search)
        )
    
    date_str = request.GET.get('date')
    if date_str:
        try:
            check_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            available_bikes = []
            for bike in bikes:
                if bike.is_available_for_date(check_date):
                    available_bikes.append(bike)
            bikes = available_bikes
        except ValueError:
            pass
    
    categories = BikeCategory.objects.filter(is_active=True)
    sizes = BikeSize.objects.all()
    
    context = {
        'bikes': bikes,
        'categories': categories,
        'sizes': sizes,
        'bike_types': Bike.BIKE_TYPES,
        'selected_category': category_slug,
        'selected_type': bike_type,
        'selected_size': size,
        'search_query': search,
        'check_date': date_str,
    }
    return render(request, 'bikes/bike_list.html', context)


def bike_detail(request, slug):
    """Bike detail view."""
    bike = get_object_or_404(
        Bike.objects.select_related('category', 'size'),
        slug=slug
    )
    
    accessories = Accessory.objects.filter(
        compatible_bikes__bike=bike,
        is_available=True
    )[:6]
    
    similar_bikes = Bike.objects.filter(
        category=bike.category,
        is_available=True
    ).exclude(id=bike.id)[:4]
    
    features = [f.strip() for f in bike.features.split('\n') if f.strip()]
    
    context = {
        'bike': bike,
        'accessories': accessories,
        'similar_bikes': similar_bikes,
        'features': features,
    }
    return render(request, 'bikes/bike_detail.html', context)

def kids_bikes(request):
    """View kids bikes."""
    bikes = Bike.objects.filter(
        bike_type='kids',
        is_available=True,
        is_maintenance=False
    ).select_related('category', 'size')
    
    context = {
        'bikes': bikes,
        'title': 'Kids Bikes',
        'description': 'Safe and fun bikes for young riders.',
    }
    return render(request, 'bikes/bike_type_list.html', context)

def bike_category(request, slug):
    """View bikes by category."""
    category = get_object_or_404(BikeCategory, slug=slug, is_active=True)
    bikes = Bike.objects.filter(
        category=category,
        is_available=True,
        is_maintenance=False
    ).select_related('size')
    
    context = {
        'category': category,
        'bikes': bikes,
    }
    return render(request, 'bikes/bike_category.html', context)

# In bikes/views.py
def adult_bikes(request):  
    """View adult bikes."""
    bikes = Bike.objects.filter(
        bike_type='adult',
        is_available=True,
        is_maintenance=False
    ).select_related('category', 'size')
    
    context = {
        'bikes': bikes,
        'title': 'Adult Bikes',
        'description': 'Premium bikes for adult riders of all skill levels.',
    }
    return render(request, 'bikes/bike_type_list.html', context)


def kids_bikes(request):
    """View kids bikes."""
    bikes = Bike.objects.filter(
        bike_type='kids',
        is_available=True,
        is_maintenance=False  
    ).select_related('category', 'size')
    
    context = {
        'bikes': bikes,
        'title': 'Kids Bikes',
        'description': 'Safe and fun bikes for young riders.',
    }
    return render(request, 'bikes/bike_type_list.html', context)


def mountain_bikes(request):
    """View mountain bikes."""
    bikes = Bike.objects.filter(
        bike_type='kids',
        is_available=True,
        is_maintenance=False  
    ).select_related('category', 'size')
    
    context = {
        'bikes': bikes,
        'title': 'Mountain Bikes',
        'description': 'Rugged bikes built for off-road adventures.',
    }
    return render(request, 'bikes/bike_type_list.html', context)


def accessories_list(request):
    """List all accessories."""
    accessories = Accessory.objects.filter(is_available=True)
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        accessories = accessories.filter(category=category)
    
    context = {
        'accessories': accessories,
        'categories': Accessory.ACCESSORY_CATEGORIES,
        'selected_category': category,
    }
    return render(request, 'bikes/accessories.html', context)


def bike_sizes_guide(request):
    """Bike sizing guide page."""
    sizes = BikeSize.objects.all()
    
    context = {
        'sizes': sizes,
    }
    return render(request, 'bikes/size_guide.html', context)
