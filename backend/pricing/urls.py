from django.urls import path
from .views import home, admin_page, PricingQuoteView
from . import api_views

urlpatterns = [
    path("", home, name="home"),
    path("admin-page/", admin_page, name="admin-page"),
    path("quote/", PricingQuoteView.as_view(), name="pricing-quote"),
    path("bikes/", api_views.bikes_list, name="bikes_list"),
    path("bikes/<int:bike_id>/", api_views.bike_update, name="bike_update"),
]