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

    # --- NEW CODE STARTS HERE ---
    
    # 1. Primary Key mapping (Fixes the Admin panel "id" crash)
    id = models.AutoField(primary_key=True, db_column="paymentid") 

    # 2. Field mappings with db_column to match your PostgreSQL table
    reservation_id = models.IntegerField(unique=True, db_column="reservationid")
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_column="amount")
    
    # Added the choices back into the mapped columns
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending", db_column="status")
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default="Mock", db_column="method")
    
    payment_date = models.DateTimeField(null=True, blank=True, db_column="paymentdate")
    created_at = models.DateTimeField(auto_now_add=True, db_column="createdat")

    class Meta:
        # 3. Ensures Django uses your existing 'payments' table
        db_table = "payments" 

    def __str__(self):
        return f"Payment(id={self.id}, reservation={self.reservation_id}, status={self.status})"
    
    
    
    
    
