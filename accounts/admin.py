from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'phone', 'is_staff', 'is_active', 'date_joined'
    ]
    list_filter = ['is_staff', 'is_active', 'is_newsletter_subscribed', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    readonly_fields = ['date_joined', 'last_login', 'created_at', 'updated_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': (
                'phone', 'address', 'city', 'state', 'zip_code',
                'date_of_birth', 'emergency_contact_name',
                'emergency_contact_phone', 'is_newsletter_subscribed',
                'admin_notes',
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
