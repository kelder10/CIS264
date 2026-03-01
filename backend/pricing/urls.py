from django.urls import path
from .views import PricingQuoteView

urlpatterns = [
    path("quote/", PricingQuoteView.as_view(), name="pricing-quote"),
]