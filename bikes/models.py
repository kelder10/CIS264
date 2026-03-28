from django.db import models
from django.urls import reverse


class BikeCategory(models.Model):
    """Model for bike categories."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Bike Category'
        verbose_name_plural = 'Bike Categories'
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('bike_category', kwargs={'slug': self.slug})


class BikeSize(models.Model):
    """Model for bike sizes with descriptions."""
    size_inches = models.PositiveIntegerField(unique=True)
    description = models.TextField(help_text="Description of who this size fits")
    recommended_height = models.CharField(max_length=100, help_text="Recommended rider height range")
    recommended_age = models.CharField(max_length=100, blank=True, help_text="Recommended age range")
    
    class Meta:
        ordering = ['size_inches']
    
    def __str__(self):
        return f"{self.size_inches}\""


class Bike(models.Model):
    """Model for bikes in inventory."""
    BIKE_TYPES = [
        ('adult', 'Adult Bike'),
        ('kids', 'Kids Bike'),
        ('mountain', 'Mountain Bike'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        BikeCategory,
        on_delete=models.CASCADE,
        related_name='bikes'
    )
    bike_type = models.CharField(max_length=20, choices=BIKE_TYPES)
    size = models.ForeignKey(
        BikeSize,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bikes'
    )
    description = models.TextField()
    features = models.TextField(help_text="List key features, one per line")
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='bikes/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_maintenance = models.BooleanField(default=False, help_text="Bike is under maintenance")
    maintenance_note = models.TextField(blank=True, help_text="Reason for maintenance")
    quantity_total = models.PositiveIntegerField(default=1, help_text="Total bikes of this model")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.size})"
    
    def get_absolute_url(self):
        return reverse('bike_detail', kwargs={'slug': self.slug})
    
    def get_available_quantity(self, date=None):
        """Get available quantity for a specific date."""
        from reservations.models import Reservation
        
        if date:
            reserved = Reservation.objects.filter(
                bike=self,
                status__in=['pending', 'confirmed', 'paid'],
                rental_date=date
            ).count()
            return max(0, self.quantity_total - reserved)
        return self.quantity_total if self.is_available and not self.is_maintenance else 0
    
    def is_available_for_date(self, date):
        """Check if bike is available for a specific date."""
        if not self.is_available or self.is_maintenance:
            return False
        return self.get_available_quantity(date) > 0
    
    @property
    def is_in_stock(self):
        """Check if bike is in stock."""
        return self.is_available and not self.is_maintenance
    
    @property
    def display_price(self):
        """Return formatted price."""
        return f"${self.price_per_day}/day"


class Accessory(models.Model):
    """Model for bike accessories."""
    ACCESSORY_CATEGORIES = [
        ('safety', 'Safety'),
        ('comfort', 'Comfort'),
        ('storage', 'Storage'),
        ('electronics', 'Electronics'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=ACCESSORY_CATEGORIES, default='other')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='accessories/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Accessory'
        verbose_name_plural = 'Accessories'
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name
    
    @property
    def display_price(self):
        """Return formatted price."""
        if self.price_per_day:
            return f"${self.price_per_day}/day"
        return f"${self.price}"


class BikeAccessory(models.Model):
    """Model linking bikes with compatible accessories."""
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='compatible_accessories')
    accessory = models.ForeignKey(Accessory, on_delete=models.CASCADE, related_name='compatible_bikes')
    is_recommended = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Bike Accessory'
        verbose_name_plural = 'Bike Accessories'
        unique_together = ['bike', 'accessory']
