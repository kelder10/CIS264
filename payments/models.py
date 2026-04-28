import uuid
from django.db import models
from django.conf import settings

from reservations.models import Reservation


class Payment(models.Model):
    """Model for simulated payments."""
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)
    
    # Payment amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Payment details
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Card info (masked for demo)
    card_last_four = models.CharField(max_length=4, blank=True)
    card_brand = models.CharField(max_length=50, blank=True)
    
    # Promo code
    promo_code = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Payment #{self.id} - ${self.total_amount} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = f"ICC-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def is_successful(self):
        return self.status == 'completed'
    
    @property
    def display_status(self):
        return self.status.replace('_', ' ').title()


class PaymentMethod(models.Model):
    """Model for saved payment methods (for demo purposes)."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_methods'
    )
    nickname = models.CharField(max_length=100, blank=True)
    card_brand = models.CharField(max_length=50)
    card_last_four = models.CharField(max_length=4)
    expiration_month = models.CharField(max_length=2)
    expiration_year = models.CharField(max_length=4)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        if self.nickname:
            return f"{self.nickname} ({self.card_brand} ...{self.card_last_four})"
        return f"{self.card_brand} ending in {self.card_last_four}"
