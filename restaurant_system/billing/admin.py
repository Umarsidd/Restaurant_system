from django.contrib import admin
from .models import Bill


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """Admin interface for Bill model"""
    
    list_display = ('id', 'table', 'order', 'total_amount', 'status', 'generated_at', 'paid_at')
    list_filter = ('status', 'generated_at')
    search_fields = ('table__table_number', 'order__id')
    readonly_fields = ('generated_at', 'paid_at', 'subtotal', 'tax_amount', 'total_amount')
    
    fieldsets = (
        ('Bill Information', {
            'fields': ('table', 'order', 'status')
        }),
        ('Payment Details', {
            'fields': ('subtotal', 'tax_percentage', 'tax_amount', 'total_amount')
        }),
        ('Staff', {
            'fields': ('cashier',)
        }),
        ('Timestamps', {
            'fields': ('generated_at', 'paid_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Recalculate totals when saving"""
        obj.calculate_totals()
        super().save_model(request, obj, form, change)
