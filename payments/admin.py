from django.contrib import admin
from .models import Payment, PaymentMethod


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'transaction_id', 'reservation', 'total_amount',
        'payment_method', 'status', 'created_at', 'processed_at'
    ]
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['transaction_id', 'reservation__user__username', 'promo_code']
    readonly_fields = ['transaction_id', 'created_at', 'processed_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Transaction', {
            'fields': ('transaction_id', 'reservation', 'status')
        }),
        ('Amounts', {
            'fields': ('subtotal', 'tax_amount', 'discount_amount', 'total_amount')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'card_brand', 'card_last_four', 'promo_code')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
    )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['user', 'nickname', 'card_brand', 'card_last_four', 'is_default', 'created_at']
    list_filter = ['card_brand', 'is_default']
    search_fields = ['user__username', 'nickname']
    readonly_fields = ['created_at']
