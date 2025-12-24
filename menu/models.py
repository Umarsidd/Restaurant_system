from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class MenuItem(models.Model):
    """Menu item model with categories"""
    
    class Category(models.TextChoices):
        STARTER = 'STARTER', 'Starter'
        MAIN = 'MAIN', 'Main Course'
        DRINKS = 'DRINKS', 'Drinks'
        DESSERT = 'DESSERT', 'Dessert'
    
    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        db_index=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'menu_items'
        ordering = ['category', 'name']
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
    def toggle_availability(self):
        """Toggle item availability"""
        self.is_available = not self.is_available
        self.save()
