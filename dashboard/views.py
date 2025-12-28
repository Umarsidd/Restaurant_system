from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta

from tables.models import Table
from orders.models import Order
from billing.models import Bill
from accounts.decorators import role_required


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """Main dashboard that redirects based on user role"""
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.is_manager:
            return redirect('dashboard:manager')
        elif user.is_cashier:
            return redirect('dashboard:cashier')
        elif user.is_waiter:
            return redirect('dashboard:waiter')
        else:
            return redirect('dashboard:table_status')


class TableStatusDashboardView(LoginRequiredMixin, TemplateView):
    """Live table status dashboard - accessible to all authenticated users"""
    template_name = 'dashboard/table_status.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all tables with their current status
        tables = Table.objects.all().order_by('table_number')
        
        # Count tables by status
        status_counts = {
            'available': tables.filter(status=Table.Status.AVAILABLE).count(),
            'occupied': tables.filter(status=Table.Status.OCCUPIED).count(),
            'bill_requested': tables.filter(status=Table.Status.BILL_REQUESTED).count(),
            'closed': tables.filter(status=Table.Status.CLOSED).count(),
        }
        
        context['tables'] = tables
        context['status_counts'] = status_counts
        context['total_tables'] = tables.count()
        
        return context


class WaiterDashboardView(LoginRequiredMixin, TemplateView):
    """Waiter-specific dashboard"""
    template_name = 'dashboard/waiter_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_waiter or request.user.is_manager):
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get waiter's active orders
        if user.is_manager:
            active_orders = Order.objects.filter(
                status__in=[Order.Status.PLACED, Order.Status.IN_KITCHEN, Order.Status.SERVED]
            )
        else:
            active_orders = Order.objects.filter(
                waiter=user,
                status__in=[Order.Status.PLACED, Order.Status.IN_KITCHEN, Order.Status.SERVED]
            )
        
        # Get available tables
        available_tables = Table.objects.filter(status=Table.Status.AVAILABLE)
        
        # Get today's orders for this waiter
        today = timezone.now().date()
        if user.is_manager:
            today_orders = Order.objects.filter(created_at__date=today)
        else:
            today_orders = Order.objects.filter(waiter=user, created_at__date=today)
        
        context['active_orders'] = active_orders[:10]
        context['available_tables'] = available_tables
        context['today_orders_count'] = today_orders.count()
        context['active_orders_count'] = active_orders.count()
        
        return context


class CashierDashboardView(LoginRequiredMixin, TemplateView):
    """Cashier-specific dashboard"""
    template_name = 'dashboard/cashier_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_cashier or request.user.is_manager):
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get pending bills
        pending_bills = Bill.objects.filter(
            status=Bill.Status.PENDING_PAYMENT
        ).order_by('-generated_at')
        
        # Get tables requesting bills (served orders without bills)
        tables_needing_bills = Table.objects.filter(
            status=Table.Status.OCCUPIED,
            orders__status=Order.Status.SERVED,
            orders__bill__isnull=True
        ).distinct()
        
        # Today's stats
        today = timezone.now().date()
        today_bills = Bill.objects.filter(generated_at__date=today)
        today_paid = today_bills.filter(status=Bill.Status.PAID)
        today_revenue = today_paid.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        context['pending_bills'] = pending_bills[:10]
        context['tables_needing_bills'] = tables_needing_bills
        context['pending_bills_count'] = pending_bills.count()
        context['today_bills_count'] = today_bills.count()
        context['today_paid_count'] = today_paid.count()
        context['today_revenue'] = today_revenue
        
        return context


class ManagerDashboardView(LoginRequiredMixin, TemplateView):
    """Manager-specific dashboard with analytics"""
    template_name = 'dashboard/manager_dashboard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        today = timezone.now().date()
        
        # Table statistics
        tables = Table.objects.all()
        context['total_tables'] = tables.count()
        context['available_tables'] = tables.filter(status=Table.Status.AVAILABLE).count()
        context['occupied_tables'] = tables.filter(status=Table.Status.OCCUPIED).count()
        
        # Today's orders
        today_orders = Order.objects.filter(created_at__date=today)
        context['today_orders_count'] = today_orders.count()
        context['active_orders_count'] = Order.objects.filter(
            status__in=[Order.Status.PLACED, Order.Status.IN_KITCHEN]
        ).count()
        
        # Today's revenue
        today_bills = Bill.objects.filter(generated_at__date=today)
        today_paid_bills = today_bills.filter(status=Bill.Status.PAID)
        today_revenue = today_paid_bills.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        context['today_bills_count'] = today_bills.count()
        context['today_paid_bills_count'] = today_paid_bills.count()
        context['today_revenue'] = today_revenue
        context['pending_bills_count'] = Bill.objects.filter(
            status=Bill.Status.PENDING_PAYMENT
        ).count()
        
        # Recent activity
        context['recent_orders'] = Order.objects.all().order_by('-created_at')[:5]
        context['recent_bills'] = Bill.objects.all().order_by('-generated_at')[:5]
        
        return context
