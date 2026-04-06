import random
import string
import qrcode

from io import BytesIO
from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.files import File
from bikes.models import Bike, Accessory
from locations.models import Location  
from django.utils import timezone
from datetime import timedelta

class ReservationAccessory(models.Model):
    """Through model for reservation accessories with quantity."""
    reservation = models.ForeignKey(
        'Reservation', 
        on_delete=models.CASCADE, 
        related_name='reservation_accessories'
    )
    accessory = models.ForeignKey(
        Accessory, 
        on_delete=models.CASCADE, 
        related_name='reservation_accessories'
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Reservation Accessory'
        verbose_name_plural = 'Reservation Accessories'
        unique_together = ['reservation', 'accessory']

    def __str__(self):
        return f"{self.quantity}x {self.accessory.name} for Reservation #{self.reservation.id}"

    def get_total(self):
        """Helper to get the cost of this line item."""
        price = self.price_at_time or Decimal('0.00')
        return price * self.quantity

    def save(self, *args, **kwargs):
        if not self.price_at_time:
            self.price_at_time = getattr(self.accessory, 'price_per_day', Decimal('0.00'))
        
        super().save(*args, **kwargs)
        
        if self.reservation:
            self.reservation.calculate_prices()
            self.reservation.save(update_fields=['accessories_price', 'subtotal', 'tax_amount', 'total_price'])

class Reservation(models.Model):
    """Model for bike reservations with Smart-Dock integration."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    RENTAL_TYPES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    # Relationships
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='reservations')
    pickup_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    
    # Security & Smart-Dock Fields
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    unlock_code = models.CharField(max_length=10, blank=True)
    
    # Rental Details
    rental_type = models.CharField(max_length=20, choices=RENTAL_TYPES, default='daily')
    rental_date = models.DateField()
    return_date = models.DateField()
    rental_duration = models.PositiveIntegerField(default=1, help_text="Duration in hours or days")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Pricing Fields
    bike_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    accessories_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Administrative & Legal
    waiver_signed = models.BooleanField(default=False)
    waiver_signed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    special_requests = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reservation #{self.id} - {self.user.username} - {self.bike.name}"

    @property
    def duration_display(self):
        """Returns a formatted string for the duration (e.g., '3 Days')."""
        duration = self.rental_duration or 1
        unit = "Hour" if self.rental_type == 'hourly' else "Day"
        plural = "s" if duration > 1 else ""
        return f"{duration} {unit}{plural}"

    def calculate_prices(self):
        """Handles all the math for the reservation and its accessories."""
        if self.rental_type == 'hourly':
            rate = getattr(self.bike, 'price_per_hour', Decimal('0.00'))
            self.bike_price = rate * Decimal(str(self.rental_duration))
        else:
            rate = getattr(self.bike, 'price_per_day', Decimal('0.00'))
            days = (self.return_date - self.rental_date).days + 1
            self.bike_price = rate * Decimal(str(max(1, days)))

        if self.pk:
            self.accessories_price = sum(
                ra.get_total() for ra in self.reservation_accessories.all()
            )
        else:
            self.accessories_price = Decimal('0.00')

        self.subtotal = self.bike_price + self.accessories_price
        self.tax_amount = (self.subtotal * Decimal('0.07')).quantize(Decimal('0.01'))
        self.total_price = self.subtotal + self.tax_amount

    def generate_qr_code(self):
        """Generates a QR code pointing to the specific unlock URL for this reservation."""
        qr_url = f"http://127.0.0.1:8000/reservations/reservation/{self.id}/unlock/" 
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        canvas = BytesIO()
        img.save(canvas, format='PNG')
        
        self.qr_code.save(f'qr_res_{self.id}.png', File(canvas), save=False)

    def save(self, *args, **kwargs):
        today = timezone.now().date()
        
        if self.rental_date < today - timedelta(days=1):
            pass 
            
        if not self.unlock_code:
            self.unlock_code = ''.join(random.choices(string.digits, k=6))
        
        self.calculate_prices()
        super().save(*args, **kwargs)

        # Generate QR code if it hasn't been created yet
        if not self.qr_code:
            self.generate_qr_code()
            # Update only the qr_code field to avoid re-running the whole save method
            super().save(update_fields=['qr_code'])
    
class Waiver(models.Model):
    """Model for rental waivers."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='waivers'
    )
    reservation = models.OneToOneField(
        'Reservation',  
        on_delete=models.CASCADE,
        related_name='waiver'
    )
    full_name = models.CharField(max_length=200)
    signature = models.CharField(max_length=200, help_text="Digital signature (typed name)")
    date_signed = models.DateTimeField(auto_now_add=True)
    acknowledged_risks = models.BooleanField(default=False)
    acknowledged_equipment = models.BooleanField(default=False)
    acknowledged_rules = models.BooleanField(default=False)
    emergency_contact_name = models.CharField(max_length=200, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ['-date_signed']

    def __str__(self):
        return f"Waiver for {self.full_name} - Reservation #{self.reservation.id}"


class PromoCode(models.Model):
    """Model for promotional codes."""
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]

    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    current_uses = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-valid_from']

    def __str__(self):
        return self.code

    def is_valid(self):
        """Check if promo code is currently valid."""
        from django.utils import timezone
        now = timezone.now()

        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_until:
            return False
        if self.max_uses and self.current_uses >= self.max_uses:
            return False
        return True

    def calculate_discount(self, subtotal):
        """Calculate discount amount."""
        if subtotal < self.minimum_order:
            return 0

        if self.discount_type == 'percentage':
            return subtotal * (self.discount_value / 100)
        return min(self.discount_value, subtotal)