from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_active = models.BooleanField(default=True)
    
    # New Capacity Fields
    total_slots = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return self.name
    
    @property
    def current_bike_count(self):
        """Counts bikes currently assigned to this location."""
        return self.bikes.count()

    @property
    def free_slots(self):
        """
        Calculates empty slots for the template. 
        Your HTML specifically calls {{ loc.free_slots }}.
        """
        slots = self.total_slots - self.current_bike_count
        return max(0, slots) # Ensures we never show negative slots

    @property
    def available_slots(self):
        """Legacy helper for logic checking."""
        return self.free_slots

    @property
    def is_full(self):
        return self.free_slots <= 0