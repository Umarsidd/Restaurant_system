from django.db import models
from django.utils import timezone


class Table(models.Model):
    """Restaurant table model with status tracking"""
    
    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', 'Available'
        OCCUPIED = 'OCCUPIED', 'Occupied'
        BILL_REQUESTED = 'BILL_REQUESTED', 'Bill Requested'
        CLOSED = 'CLOSED', 'Closed'
    
    table_number = models.CharField(max_length=10, unique=True, db_index=True)
    seating_capacity = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
        db_index=True
    )
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'tables'
        ordering = ['table_number']
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'
    
    def __str__(self):
        return f"Table {self.table_number}"
    
    def mark_as_occupied(self):
        """Mark table as occupied"""
        self.status = self.Status.OCCUPIED
        self.save()
    
    def mark_as_available(self):
        """Mark table as available"""
        self.status = self.Status.AVAILABLE
        self.save()
    
    def request_bill(self):
        """Mark table as waiting for bill"""
        self.status = self.Status.BILL_REQUESTED
        self.save()
    
    @property
    def is_available(self):
        return self.status == self.Status.AVAILABLE
    
    @property
    def is_occupied(self):
        return self.status == self.Status.OCCUPIED
    
    @property
    def current_order(self):
        """Get the current active order for this table"""
        from orders.models import Order
        return Order.objects.filter(
            table=self,
            status__in=[Order.Status.PLACED, Order.Status.IN_KITCHEN, Order.Status.SERVED]
        ).first()
