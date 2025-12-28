from django.contrib import admin
from .models import Table


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """Admin interface for Table model"""
    
    list_display = ('table_number', 'seating_capacity', 'status', 'last_activity')
    list_filter = ('status',)
    search_fields = ('table_number',)
    readonly_fields = ('last_activity', 'created_at')
    
    fieldsets = (
        ('Table Information', {
            'fields': ('table_number', 'seating_capacity')
        }),
        ('Status', {
            'fields': ('status', 'last_activity')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
