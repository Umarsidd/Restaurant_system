"""
Role-based access control decorators
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """
    Decorator to check if user has required role(s)
    Usage: @role_required('WAITER')
           @role_required('WAITER', 'MANAGER')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped_view(request, *args, **kwargs):
            if request.user.role in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You don't have permission to access this page.")
            raise PermissionDenied
        return wrapped_view
    return decorator


def waiter_required(view_func):
    """Decorator for waiter-only views"""
    return role_required('WAITER')(view_func)


def cashier_required(view_func):
    """Decorator for cashier-only views"""
    return role_required('CASHIER')(view_func)


def manager_required(view_func):
    """Decorator for manager-only views"""
    return role_required('MANAGER')(view_func)


def staff_required(view_func):
    """Decorator for any staff member (waiter, cashier, manager)"""
    return role_required('WAITER', 'CASHIER', 'MANAGER')(view_func)
