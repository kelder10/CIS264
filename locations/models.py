from django.db import models
from django.utils import timezone

class Location(models.Model):
    # --- Basic Fields ---
    name = models.CharField(max_length=100)
    station_number = models.IntegerField(default=0)
    address = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_active = models.BooleanField(default=True)
    total_slots = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return self.name
    
    # --- Capacity Properties ---
    @property
    def current_bike_count(self):
        """Total bikes physically sitting in docks at this location."""
        return self.bikes.count()

    @property
    def free_slots(self):
        """Empty docks available for incoming returns."""
        slots = self.total_slots - self.current_bike_count
        return max(0, slots)
    free_slots.fget.short_description = "Available Slots"

    @property
    def is_full(self):
        """Flag for UI and return-logic blocking."""
        return self.free_slots <= 0

    # --- Logistics & Dispatch Helpers ---

    @property
    def status_level(self):
        """Dashboard color coding: Red (Full), Yellow (Almost Full), Green (Open)."""
        if self.is_full:
            return "danger"
        # If 80% or more of slots are filled, show a warning
        if self.current_bike_count >= (self.total_slots * 0.8):
            return "warning"
        return "success"

    @property
    def needs_pickup_dispatch(self):
        """
        Logic for the Driver:
        1. Never flag the Hub for pickup (bikes go TO the Hub).
        2. Flag if the trailhead has bikes waiting to be returned to base.
        """
        # Exclude the warehouse/hub
        if "Main Shop" in self.name or "Hub" in self.name:
            return False
            
        # Trigger if there is even 1 bike sitting at a trailhead for pickup
        return self.current_bike_count > 0

    @property
    def collection_priority(self):
        """Tells the driver which trailhead to hit first."""
        if self.is_full:
            return "URGENT"
        if self.current_bike_count >= (self.total_slots - 2):
            return "HIGH"
        if self.needs_pickup_dispatch:
            return "SCHEDULED"
        return "NONE"