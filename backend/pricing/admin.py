from django.contrib import admin
from .models import Bike, Reservation, User, BikeType, RentalLocation, Trail


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ("bike_id", "type", "size", "hourly_rate", "status", "location")
    list_filter = ("type", "status", "size", "location")
    search_fields = ("bike_id",)
    ordering = ("bike_id",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("user_id", "name", "email", "birthday")
    search_fields = ("name", "email")
    ordering = ("name",)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "reservation_id",
        "user",
        "bike",
        "start_date",
        "end_date",
        "status",
        "total_cost",
        "location",
        "trail",
    )
    list_filter = ("status", "start_date", "location")
    search_fields = (
        "reservation_id",
        "user__name",
        "user__email",
        "bike__bike_id",
    )
    ordering = ("-start_date",)


# Optional: register lookup tables so you can manage them too
admin.site.register(BikeType)
admin.site.register(RentalLocation)
admin.site.register(Trail)