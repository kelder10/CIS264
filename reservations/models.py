from decimal import Decimal
from django.db import models
from django.urls import reverse
from django.conf import settings

from bikes.models import Bike, Accessory


class Reservation(models.Model):
    """Model for bike reservations."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    RENTAL_TYPES = [
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    bike = models.ForeignKey(
        Bike,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    accessories = models.ManyToManyField(
        Accessory,
        through='ReservationAccessory',
        blank=True,
        related_name='reservations'
    )

    # Rental details
    rental_type = models.CharField(max_length=20, choices=RENTAL_TYPES, default='daily')
    rental_date = models.DateField()
    return_date = models.DateField()
    rental_duration = models.PositiveIntegerField(help_text="Duration in hours or days")

    # Status and pricing
    bike_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    accessories_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Waiver
    waiver_signed = models.BooleanField(default=False)
    waiver_signed_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Notes
    special_requests = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reservation #{self.id} - {self.user.get_full_name()} - {self.bike.name}"

    def get_absolute_url(self):
        return reverse('reservation_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        """
        Save reservation normally.

        Do NOT call calculate_prices() here, because a new reservation may not
        have a primary key yet, and accessory relationships cannot be used until
        the reservation is saved in the database.
        """
        super().save(*args, **kwargs)

    def calculate_prices(self):
        """Calculate reservation prices safely."""
        # Bike price
        if self.rental_type == 'hourly' and self.bike.price_per_hour:
            self.bike_price = self.bike.price_per_hour * self.rental_duration
        else:
            # Default to daily pricing
            days = (self.return_date - self.rental_date).days + 1
            self.bike_price = self.bike.price_per_day * max(1, days)

        # Accessories price
        # Only use related accessories if reservation already exists in DB
        if self.pk:
            self.accessories_price = sum(
                ra.calculate_price() for ra in self.reservation_accessories.all()
            )
        else:
            self.accessories_price = Decimal('0.00')

        # Subtotal and total
        self.subtotal = self.bike_price + self.accessories_price
        self.tax_amount = self.subtotal * Decimal('0.07')  # 7% tax
        self.total_price = self.subtotal + self.tax_amount

    @property
    def is_active(self):
        """Check if reservation is active."""
        return self.status in ['pending', 'confirmed', 'paid']

    @property
    def is_paid(self):
        """Check if reservation is paid."""
        return self.status == 'paid'

    @property
    def duration_display(self):
        """Return human-readable duration."""
        if self.rental_type == 'hourly':
            return f"{self.rental_duration} hour{'s' if self.rental_duration > 1 else ''}"
        days = (self.return_date - self.rental_date).days + 1
        return f"{days} day{'s' if days > 1 else ''}"


class ReservationAccessory(models.Model):
    """Through model for reservation accessories with quantity."""
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='reservation_accessories'
    )
    accessory = models.ForeignKey(
        Accessory,
        on_delete=models.CASCADE,
        related_name='reservation_accessories'
    )
    quantity = models.PositiveIntegerField(default=1)
    price_at_time = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = 'Reservation Accessory'
        verbose_name_plural = 'Reservation Accessories'
        unique_together = ['reservation', 'accessory']

    def __str__(self):
        return f"{self.quantity}x {self.accessory.name} for Reservation #{self.reservation.id}"

    def calculate_price(self):
        """Calculate total price for this accessory."""
        if self.accessory.price_per_day:
            days = (self.reservation.return_date - self.reservation.rental_date).days + 1
            return self.accessory.price_per_day * self.quantity * max(1, days)
        return self.accessory.price * self.quantity

    def save(self, *args, **kwargs):
        # Store price at time of reservation
        if not self.price_at_time:
            if self.accessory.price_per_day:
                self.price_at_time = self.accessory.price_per_day
            else:
                self.price_at_time = self.accessory.price
        super().save(*args, **kwargs)


class Waiver(models.Model):
    """Model for rental waivers."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='waivers'
    )
    reservation = models.OneToOneField(
        Reservation,
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