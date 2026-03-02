from django.urls import path
from django.http import JsonResponse
from .views import PayReservationView

def payments_root(request):
    return JsonResponse({"ok": True, "endpoints": ["/api/payments/pay/"]}) #add for no response
urlpatterns = [
    path("", payments_root),
    path("pay/", PayReservationView.as_view(), name="pay-reservation"),
]