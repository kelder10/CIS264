from django.contrib import admin
from .models import ContactInquiry, Trail, SiteSetting

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'inquiry_type', 'created_at', 'is_resolved']
    list_filter = ['inquiry_type', 'is_resolved', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_resolved']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Inquiry Details', {
            'fields': ('inquiry_type', 'planned_date', 'group_size', 'message')
        }),
        ('Status', {
            'fields': ('is_resolved', 'created_at')
        }),
    )


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty', 'length_miles', 'estimated_time', 'is_featured']
    list_filter = ['difficulty', 'is_featured']
    search_fields = ['name', 'description', 'highlights']
    list_editable = ['is_featured']
    
    fieldsets = (
        ('Trail Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Trail Details', {
            'fields': ('difficulty', 'length_miles', 'estimated_time', 'terrain')
        }),
        ('Highlights', {
            'fields': ('highlights',)
        }),
        ('Display Options', {
            'fields': ('is_featured',)
        }),
    )


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['key', 'description']
    search_fields = ['key', 'description']
