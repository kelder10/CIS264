from django.contrib import admin
from django.db import models  
from .models import Reservation, ReservationAccessory, Waiver, PromoCode

class ReservationAccessoryInline(admin.TabularInline):
    model = ReservationAccessory
    extra = 0
    readonly_fields = ['price_at_time']
    fields = ['accessory', 'fulfillment_type', 'quantity', 'price_at_time']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'bike', 'rental_date', 'return_date',
        'status', 'total_price', 'waiver_signed', 'created_at'
    ]
    list_filter = ['status', 'rental_type', 'waiver_signed', 'created_at']
    search_fields = ['user__username', 'user__email', 'bike__name']
    readonly_fields = ['created_at', 'updated_at', 'calculated_prices_display']
    inlines = [ReservationAccessoryInline] # Kept this here once
    date_hierarchy = 'rental_date'
    
    fieldsets = (
        ('Reservation Info', {
            'fields': ('user', 'bike', 'status')
        }),
        ('Rental Details', {
            'fields': ('rental_type', 'rental_date', 'return_date', 'rental_duration')
        }),
        ('Pricing', {
            'fields': ('calculated_prices_display', 'bike_price', 'accessories_price', 'subtotal', 'tax_amount', 'total_price')
        }),
        ('Waiver', {
            'fields': ('waiver_signed', 'waiver_signed_at')
        }),
        ('Notes', {
            'fields': ('special_requests', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    
    def calculated_prices_display(self, obj):
        return f"Bike: ${obj.bike_price} | Accessories: ${obj.accessories_price} | Subtotal: ${obj.subtotal} | Tax: ${obj.tax_amount} | Total: ${obj.total_price}"
    
    calculated_prices_display.short_description = 'Price Breakdown'
    
    def save_formset(self, request, form, formset, change):
        """
        This is the magic fix: It saves the inline accessories FIRST, 
        then tells the reservation to calculate the totals.
        """
        instances = formset.save()
        form.instance.calculate_prices()
        
    


@admin.register(Waiver)
class WaiverAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'reservation', 'date_signed']
    search_fields = ['full_name', 'user__username', 'reservation__id']
    readonly_fields = ['date_signed']


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'discount_type', 'discount_value',
        'valid_from', 'valid_until', 'current_uses', 'max_uses', 'is_active', 'is_valid'
    ]
    list_filter = ['discount_type', 'is_active']
    search_fields = ['code', 'description']
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Currently Valid'
