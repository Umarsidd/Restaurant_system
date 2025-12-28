from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with role-based access control"""
    
    class Role(models.TextChoices):
        WAITER = 'WAITER', 'Waiter'
        CASHIER = 'CASHIER', 'Cashier'
        MANAGER = 'MANAGER', 'Manager'
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.WAITER
    )
    phone_number = models.CharField(max_length=15, blank=True)
    employee_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_waiter(self):
        return self.role == self.Role.WAITER
    
    @property
    def is_cashier(self):
        return self.role == self.Role.CASHIER
    
    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER
