from django.urls import path
from django.contrib.auth import views as auth_views 
from .views import (
    home, admin_page, PricingQuoteView, adults, kids, 
    trail_info, about, accessories, waiver, 
    bike_inventory, reservations, availability,
    add_to_cart, cart_view  # <-- Make sure cart_view is here, not cart
)
from . import api_views

urlpatterns = [
    path("", home, name="home"),
    path("adults/", adults, name="adults"),          
    path("kids/", kids, name="kids"),                
    path("accessories/", accessories, name="accessories"), 
    path("trail-info/", trail_info, name="trail-info"), 
    path("waiver/", waiver, name="waiver"),
    path("about/", about, name="about"),
    
    # Change the middle part to cart_view to match your import
    path("cart/", cart_view, name="cart"), 

    path("admin-page/inventory/", bike_inventory, name="bike-inventory"),
    path("admin-page/reservations/", reservations, name="reservations"),
    path("admin-page/availability/", availability, name="availability"),
    
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("admin-page/", admin_page, name="admin-page"),

    path("quote/", PricingQuoteView.as_view(), name="pricing-quote"),
    path("bikes/", api_views.bikes_list, name="bikes_list"),
    path("bikes/<int:bike_id>/", api_views.bike_update, name="bike_update"),
    
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
]