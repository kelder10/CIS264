from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "reservation_id",
        "amount",
        "status",
        "method",
        "payment_date",
        "created_at",
    )
    list_filter = ("status", "method", "payment_date", "created_at")
    search_fields = ("reservation_id",)
    ordering = ("-created_at",)