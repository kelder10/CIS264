from django.urls import path
from .views import PricingQuoteView
from . import api_views

urlpatterns = [
    path("quote/", PricingQuoteView.as_view(), name="pricing-quote"),
    
     # Inventory API
    path("api/bikes/", api_views.bikes_list, name="bikes_list"),
    # if you made an update endpoint:
    path("api/bikes/<int:bike_id>/", api_views.bike_update, name="bike_update"),
]
