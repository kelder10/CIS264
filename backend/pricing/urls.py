from django.urls import path
from .views import admin_page
from .views import PricingQuoteView
from . import api_views

urlpatterns = [
    path("admin-page/", admin_page, name="admin-page"),
    
    path("quote/", PricingQuoteView.as_view(), name="pricing-quote"),
 
     # Inventory API
    path("bikes/", api_views.bikes_list, name="bikes_list"),
    # if you made an update endpoint:
    path("bikes/<int:bike_id>/", api_views.bike_update, name="bike_update"),
]
