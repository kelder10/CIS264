import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from .models import Bike, BikeType, Trail, RentalLocation, Accessory
from .services import calculate_total_cost

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# --- BASIC NAVIGATION VIEWS ---

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def accessories(request):
    all_accessories = Accessory.objects.all()
    equipment_keywords = ['Helmet', 'Lock', 'Pannier', 'Lights', 'Vest', 'Bag']
    
    equipment_addons = []
    trail_essentials = []

    for item in all_accessories:
        if any(key.lower() in item.name.lower() for key in equipment_keywords):
            equipment_addons.append(item)
        else:
            trail_essentials.append(item)

    return render(request, "accessories.html", {
        "equipment_addons": equipment_addons,
        "trail_essentials": trail_essentials,
    })

def trail_info(request):
    trails = Trail.objects.all()
    return render(request, "trail_info.html", {"trails": trails})

def waiver(request):
    return render(request, "waiver.html")

# --- CART LOGIC ---

def add_to_cart(request):
    if request.method == "POST":
        # Check both potential names to be safe
        item_id = request.POST.get('bike_id') or request.POST.get('item_id')
        duration = int(request.POST.get('duration', 1))
        item_type = request.POST.get('item_type', 'bike') 
        
        cart = request.session.get('cart', [])

        if item_type == 'bike':
            bike = Bike.objects.get(bike_id=item_id)
            cart_item = {
                'item_id': item_id,
                'item_type': 'bike',
                'title': bike.type.type_name if bike.type else "Bike",
                'subtitle': bike.name,
                'size': bike.size,
                'price': float(bike.hourly_rate),
                'duration': duration, 
                'line_total': float(bike.hourly_rate) * duration
            }
        else:
            # Matches your old project's database field name: accessory_id
            acc = Accessory.objects.get(accessory_id=item_id)
            cart_item = {
                'item_id': item_id,
                'item_type': 'accessory',
                'title': acc.name,
                'subtitle': "Accessory",
                'size': "N/A",
                'price': float(acc.price),
                'duration': 1,
                'line_total': float(acc.price)
            }

        cart.append(cart_item)
        request.session['cart'] = cart
        request.session.modified = True
        
        return redirect(request.META.get('HTTP_REFERER', 'cart'))
    
    return redirect('home')

def cart_view(request):
    # Get the current raw cart from the session
    session_cart = request.session.get('cart', [])
    
    # HANDLE REMOVAL FIRST
    if request.method == "POST" and request.POST.get('action') == 'remove':
        index = request.POST.get('index')
        if index is not None:
            idx = int(index)
            if 0 <= idx < len(session_cart):
                session_cart.pop(idx)
                request.session['cart'] = session_cart
                request.session.modified = True
        return redirect('cart')

    # PREPARE DISPLAY DATA
    cart_items = []
    total_cost = 0
    equipment_keywords = ['Helmet', 'Lock', 'Pannier', 'Lights', 'Vest', 'Bag']

    for item in session_cart:
        target_id = item.get('item_id')
        item_type = item.get('item_type')
        
        display_title = ""
        display_subtitle = ""
        price = 0
        is_rental = True # Default for bikes

        if item_type == 'accessory':
            acc = Accessory.objects.filter(accessory_id=target_id).first()
            if acc:
                display_title = acc.name 
                price = acc.price
                if any(key.lower() in acc.name.lower() for key in equipment_keywords):
                    display_subtitle = "Rental - Return after trip"
                else:
                    display_subtitle = "Purchase - Yours to keep"
                
                # We set this to False for ALL accessories so duration stays hidden
                is_rental = False 
        else:
            bike = Bike.objects.filter(bike_id=target_id).first()
            if bike:
                display_title = bike.type.type_name if bike.type else "Bike"
                display_subtitle = f"{bike.name} (Rental)"
                price = bike.hourly_rate
                is_rental = True # Bikes show duration

        # Get the duration from the session item (defaults to 1)
        duration_val = int(item.get('duration', 1))
        
        # Logic for price and duration display
        if is_rental:
            line_total = float(price) * duration_val
            display_duration = f"{duration_val} Hour(s)"
        else:
            # Accessories fall here: price is flat, and duration text is hidden
            line_total = float(price)
            display_duration = None 

        total_cost += line_total
        
        # Add to the list we send to the HTML
        cart_items.append({
            'title': display_title,
            'subtitle': display_subtitle,
            'duration': display_duration,
            'line_total': "{:.2f}".format(line_total) 
        })

    return render(request, "cart.html", {
        'cart_items': cart_items, 
        'total_cost': "{:.2f}".format(total_cost)
    })
    
# --- BIKE LIST VIEWS ---

def adults(request):
    zip_query = request.GET.get('zipcode')
    all_adult_bikes = Bike.objects.filter(type__category='Adult', is_available=True)
    groups = {}
    for bike in all_adult_bikes:
        group_key = bike.type.pk 
        if group_key not in groups:
            groups[group_key] = {'details': bike, 'sizes': []}
        groups[group_key]['sizes'].append(bike)

    trails = Trail.objects.filter(zip_code__icontains=zip_query.strip()) if zip_query else []

    return render(request, "adults.html", {
        "grouped_bikes": groups.values(),
        "trails": trails,
        "zip_used": zip_query
    })

def kids(request):
    zip_query = request.GET.get('zipcode')
    all_kids_bikes = Bike.objects.filter(type__category='Kids', is_available=True)
    groups = {}
    for bike in all_kids_bikes:
        group_key = bike.type.pk 
        if group_key not in groups:
            groups[group_key] = {'details': bike, 'sizes': []}
        groups[group_key]['sizes'].append(bike)

    trails = Trail.objects.filter(zip_code__icontains=zip_query.strip()) if zip_query else []

    return render(request, "kids.html", {
        "grouped_bikes": groups.values(),
        "trails": trails,
        "zip_used": zip_query
    })

# --- ADMIN VIEWS ---

@login_required(login_url='login')
def admin_page(request): return render(request, "admin.html")

@login_required(login_url='login')
def bike_inventory(request): return render(request, "bike_inventory.html")

@login_required(login_url='login')
def reservations(request): return render(request, "reservations.html")

@login_required(login_url='login')
def availability(request): return render(request, "availability.html")

# --- API VIEWS (RESTORED) ---

class PricingQuoteView(APIView):
    def post(self, request):
        try:
            raw_body = request.body.decode("utf-8-sig").strip()
            data = json.loads(raw_body) if raw_body else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            return Response({"error": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST)

        hourly_rate = data.get("hourly_rate")
        start_date = parse_datetime(data.get("start_date"))
        end_date = parse_datetime(data.get("end_date"))
        promo_code = data.get("promo_code")

        if None in [hourly_rate, start_date, end_date]:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = calculate_total_cost(hourly_rate, start_date, end_date, promo_code)
            return Response(result, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)