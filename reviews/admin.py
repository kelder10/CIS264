from django.contrib import admin
from .models import Review, ReviewImage, ReviewHelpfulVote


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'bike', 'rating', 'title', 'is_approved',
        'is_featured', 'helpful_count', 'created_at'
    ]
    list_filter = ['rating', 'is_approved', 'is_featured', 'created_at']
    search_fields = ['user__username', 'title', 'content']
    list_editable = ['is_approved', 'is_featured']
    readonly_fields = ['helpful_count', 'created_at', 'updated_at']
    inlines = [ReviewImageInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Review Info', {
            'fields': ('user', 'bike', 'rating', 'title', 'content')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_featured', 'admin_response', 'admin_response_date')
        }),
        ('Engagement', {
            'fields': ('helpful_count',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if 'admin_response' in form.changed_data and obj.admin_response:
            from django.utils import timezone
            obj.admin_response_date = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ['review', 'caption', 'uploaded_at']
    search_fields = ['review__title', 'caption']


@admin.register(ReviewHelpfulVote)
class ReviewHelpfulVoteAdmin(admin.ModelAdmin):
    list_display = ['review', 'user', 'created_at']
    search_fields = ['review__title', 'user__username']
