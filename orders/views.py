from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.db import transaction

from .models import Order, OrderItem
from tables.models import Table
from menu.models import MenuItem
from accounts.decorators import role_required


class OrderListView(LoginRequiredMixin, ListView):
    """List all orders - filtered for waiters"""
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.all().select_related('table', 'waiter')
        
        # Waiters only see their own orders
        if user.is_waiter and not user.is_manager:
            queryset = queryset.filter(waiter=user)
        
        # Filter by status if provided
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')


class OrderCreateView(LoginRequiredMixin, CreateView):
    """Create a new order"""
    model = Order
    template_name = 'orders/order_create.html'
    fields = ['table', 'notes']
    success_url = reverse_lazy('orders:list')
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_waiter or request.user.is_manager):
            messages.error(request, "You don't have permission to create orders.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_tables'] = Table.objects.filter(status=Table.Status.AVAILABLE)
        context['menu_items'] = MenuItem.objects.filter(is_available=True).order_by('category', 'name')
        return context
    
    def form_valid(self, form):
        form.instance.waiter = self.request.user
        
        with transaction.atomic():
            self.object = form.save()
            
            # Add order items from POST data
            for key, quantity in self.request.POST.items():
                if key.startswith('item_') and int(quantity or 0) > 0:
                    menu_item_id = key.replace('item_', '')
                    menu_item = MenuItem.objects.get(id=menu_item_id)
                    OrderItem.objects.create(
                        order=self.object,
                        menu_item=menu_item,
                        quantity=int(quantity),
                        price_at_order=menu_item.price
                    )
        
        messages.success(self.request, f"Order created successfully for {self.object.table}")
        return redirect(self.success_url)


class OrderDetailView(LoginRequiredMixin, DetailView):
    """View order details"""
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        # Waiters can only view their own orders
        if user.is_waiter and not user.is_manager:
            queryset = queryset.filter(waiter=user)
        
        return queryset


class OrderUpdateStatusView(LoginRequiredMixin, UpdateView):
    """Update order status"""
    model = Order
    fields = []
    template_name = 'orders/order_update_status.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_waiter or request.user.is_manager):
            messages.error(request, "You don't have permission to update orders.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.Status.choices):
            self.object.status = new_status
            self.object.save()
            messages.success(request, f"Order status updated to {self.object.get_status_display()}")
        else:
            messages.error(request, "Invalid status")
        
        return redirect('orders:detail', pk=self.object.pk)
