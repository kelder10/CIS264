from django.contrib import admin
from .models import BikeCategory, BikeSize, Bike, Accessory, BikeAccessory


class BikeAccessoryInline(admin.TabularInline):
    model = BikeAccessory
    extra = 1
    autocomplete_fields = ['accessory']


@admin.register(BikeCategory)
class BikeCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'display_order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['display_order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BikeSize)
class BikeSizeAdmin(admin.ModelAdmin):
    list_display = ['size_inches', 'recommended_height', 'recommended_age']
    search_fields = ['size_inches', 'description']


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'bike_type', 'size',
        'price_per_day', 'is_available', 'is_maintenance', 'quantity_total'
    ]
    list_filter = ['category', 'bike_type', 'is_available', 'is_maintenance']
    search_fields = ['name', 'description', 'features']
    list_editable = ['is_available', 'is_maintenance', 'price_per_day']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BikeAccessoryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'bike_type', 'size')
        }),
        ('Description', {
            'fields': ('description', 'features')
        }),
        ('Pricing', {
            'fields': ('price_per_day', 'price_per_hour')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Availability', {
            'fields': ('is_available', 'is_maintenance', 'maintenance_note', 'quantity_total')
        }),
    )


@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'price_per_day', 'is_available', 'quantity_in_stock']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'price']


@admin.register(BikeAccessory)
class BikeAccessoryAdmin(admin.ModelAdmin):
    list_display = ['bike', 'accessory', 'is_recommended']
    list_filter = ['is_recommended']
    search_fields = ['bike__name', 'accessory__name']
