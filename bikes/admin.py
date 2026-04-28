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
        'name', 'serial_number', 'category', 'location', 'display_status', 
        'price_per_day', 'is_available', 'is_maintenance'
    ]
    
    list_filter = ['category', 'location', 'status', 'is_available'] 
    
    # Allows you to quickly find a specific bike by scanning or typing the serial number
    search_fields = ['name', 'serial_number', 'description', 'features']
    
    # Allows quick updates directly from the list view
    list_editable = ['is_available', 'is_maintenance', 'price_per_day']
    
    prepopulated_fields = {'slug': ('name',)}
    inlines = [BikeAccessoryInline]
    
    def display_status(self, obj):
        return obj.display_status
    display_status.short_description = 'Status'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'serial_number', 'slug', 'category', 'bike_type', 'size')
        }),
        ('Smart-Dock System', {
            'fields': ('location', 'status')
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
            'fields': ('is_available', 'is_maintenance', 'maintenance_note') 
        }),
    )

@admin.register(Accessory)
class AccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_per_day', 'is_available', 'quantity_in_stock']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']
    list_editable = ['is_available', 'price_per_day'] 
    

@admin.register(BikeAccessory)
class BikeAccessoryAdmin(admin.ModelAdmin):
    list_display = ['bike', 'accessory', 'is_recommended']
    list_filter = ['is_recommended']
    search_fields = ['bike__name', 'accessory__name']

