from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline for order items"""
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)
    fields = ('menu_item', 'quantity', 'price_at_order', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model"""
    
    list_display = ('id', 'table', 'waiter', 'status', 'created_at', 'order_total')
    list_filter = ('status', 'created_at')
    search_fields = ('table__table_number', 'waiter__username')
    readonly_fields = ('created_at', 'updated_at', 'order_total')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('table', 'waiter', 'status', 'notes')
        }),
        ('Total', {
            'fields': ('order_total',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def order_total(self, obj):
        """Display order total"""
        return f"₹{obj.calculate_total():.2f}"
    order_total.short_description = 'Total'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model"""
    
    list_display = ('order', 'menu_item', 'quantity', 'price_at_order', 'subtotal')
    list_filter = ('menu_item__category',)
    search_fields = ('order__id', 'menu_item__name')
