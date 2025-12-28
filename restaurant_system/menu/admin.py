from django.contrib import admin
from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """Admin interface for MenuItem model"""
    
    list_display = ('name', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('is_available',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Item Information', {
            'fields': ('name', 'category', 'price', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Availability', {
            'fields': ('is_available',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
