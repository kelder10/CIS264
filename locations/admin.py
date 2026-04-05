from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'zip_code', 'available_slots', 'total_slots', 'is_active')
    list_filter = ('is_active', 'zip_code')
    search_fields = ('name', 'address')


