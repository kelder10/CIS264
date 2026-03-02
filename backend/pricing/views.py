from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import json
from django.utils.dateparse import parse_datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .services import calculate_total_cost

@login_required
def admin_page(request):
    return render(request, "pricing/admin.html")
class PricingQuoteView(APIView):
    """
    MVP: quote endpoint.
    For now we accept hourly_rate directly.
    Later we will fetch hourly_rate from Bikes table/model.
    """

    def post(self, request):
        # --- Fix: accept UTF-8 with BOM (PowerShell often writes BOM) ---
        try:
            raw_body = request.body.decode("utf-8-sig").strip()
            data = json.loads(raw_body) if raw_body else {}
        except json.JSONDecodeError as e:
            return Response(
                {"error": f"Invalid JSON body: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except UnicodeDecodeError as e:
            return Response(
                {"error": f"Invalid encoding (expected UTF-8): {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        hourly_rate = data.get("hourly_rate")
        start_date = parse_datetime(data.get("start_date"))
        end_date = parse_datetime(data.get("end_date"))
        promo_code = data.get("promo_code")

        if hourly_rate is None or start_date is None or end_date is None:
            return Response(
                {"error": "hourly_rate, start_date, end_date are required (ISO datetime)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = calculate_total_cost(hourly_rate, start_date, end_date, promo_code)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)