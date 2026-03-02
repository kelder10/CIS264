import json
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods
from django.utils import timezone
#from rest_framework.views import APIView
#from rest_framework.response import Response
#from rest_framework import status

from .models import Payment

class PayReservationView(APIView):
    """
    MVP: record a payment for a reservation_id.
    """
    def post(self, request):
        reservation_id = request.data.get("reservation_id")
        amount = request.data.get("amount")
        method = request.data.get("method", "Mock")

        if reservation_id is None or amount is None:
            return Response(
                {"error": "reservation_id and amount are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment, _created = Payment.objects.get_or_create(
            reservation_id=reservation_id,
            defaults={"amount": amount, "status": "Pending", "method": method},
        )

        # MVP: mark paid immediately
        payment.amount = amount
        payment.method = method
        payment.status = "Paid"
        payment.payment_date = timezone.now()
        payment.save()

        return Response(
            {
                "payment_id": payment.id,
                "reservation_id": payment.reservation_id,
                "amount": str(payment.amount),
                "status": payment.status,
                "method": payment.method,
            },
            status=status.HTTP_200_OK,
        )