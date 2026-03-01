from django.urls import path
from .views import PayReservationView

urlpatterns = [
    path("pay/", PayReservationView.as_view(), name="pay-reservation"),
]