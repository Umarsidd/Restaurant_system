from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from decimal import Decimal


class Order(models.Model):
    """Order model for tracking table orders"""
    
    class Status(models.TextChoices):
        PLACED = 'PLACED', 'Placed'
        IN_KITCHEN = 'IN_KITCHEN', 'In Kitchen'
        SERVED = 'SERVED', 'Served'
    
    table = models.ForeignKey('tables.Table', on_delete=models.CASCADE, related_name='orders')
    waiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='orders')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLACED,
        db_index=True
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def __str__(self):
        return f"Order #{self.pk} - Table {self.table.table_number}"
    
    def calculate_total(self):
        """Calculate total order amount"""
        return sum(item.subtotal for item in self.items.all())
    
    def move_to_kitchen(self):
        """Move order to kitchen"""
        self.status = self.Status.IN_KITCHEN
        self.save()
    
    def mark_served(self):
        """Mark order as served"""
        self.status = self.Status.SERVED
        self.save()
    
    def save(self, *args, **kwargs):
        """Override save to update table status"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.table.status == 'AVAILABLE':
            self.table.mark_as_occupied()


class OrderItem(models.Model):
    """Individual items in an order"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey('menu.MenuItem', on_delete=models.PROTECT, related_name='order_items')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price snapshot at the time of order"
    )
    
    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.quantity * self.price_at_order
    
    def update_quantity(self, quantity):
        """Update item quantity"""
        self.quantity = quantity
        self.save()
    
    def save(self, *args, **kwargs):
        """Override save to capture price snapshot"""
        if not self.price_at_order:
            self.price_at_order = self.menu_item.price
        super().save(*args, **kwargs)
