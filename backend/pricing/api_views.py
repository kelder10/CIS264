import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .models import Bike, BikeType, RentalLocation


@require_http_methods(["GET"])
def bikes_list(request):
    bikes = Bike.objects.select_related("type", "location").order_by("bike_id")
    data = []
    for b in bikes:
        data.append({
            "bike_id": b.bike_id,
            "type_id": b.type.type_id,
            "type_name": b.type.type_name,
            "location_id": b.location.location_id,
            "location_name": b.location.location_name,
            "size": b.size,
            "hourly_rate": float(b.hourly_rate),
            "status": b.status,
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
@staff_member_required
@require_http_methods(["PATCH"])
def bike_update(request, bike_id: int):
    bike = get_object_or_404(Bike, bike_id=bike_id)
    payload = json.loads(request.body.decode("utf-8") or "{}")

    # update allowed fields if provided
    if "status" in payload:
        allowed = {"Available", "Unavailable", "Maintenance"}
        if payload["status"] not in allowed:
            return JsonResponse({"error": f"status must be one of {sorted(allowed)}"}, status=400)
        bike.status = payload["status"]

    if "hourly_rate" in payload:
        bike.hourly_rate = payload["hourly_rate"]

    if "size" in payload:
        bike.size = payload["size"]

    if "type_id" in payload:
        bike.type = get_object_or_404(BikeType, type_id=payload["type_id"])

    if "location_id" in payload:
        bike.location = get_object_or_404(RentalLocation, location_id=payload["location_id"])

    bike.save()
    return JsonResponse({"ok": True, "bike_id": bike.bike_id})