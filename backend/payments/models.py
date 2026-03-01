from django.db import models

class Payment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
    ]

    METHOD_CHOICES = [
        ("Mock", "Mock"),
        ("Card", "Card"),
        ("Cash", "Cash"),
        ("Online", "Online"),
    ]

    # We store ReservationID as an integer for now so you can work
    # even if reservations app/model isn't added yet.
    reservation_id = models.IntegerField(unique=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default="Mock")
    payment_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment(reservation_id={self.reservation_id}, status={self.status})"