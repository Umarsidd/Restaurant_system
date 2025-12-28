from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, View
from django.http import HttpResponse
from django.db import transaction
from django.utils import timezone

from .models import Bill
from orders.models import Order
from tables.models import Table


class BillListView(LoginRequiredMixin, ListView):
    """List all bills"""
    model = Bill
    template_name = 'billing/bill_list.html'
    context_object_name = 'bills'
    paginate_by = 20
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_cashier or request.user.is_manager):
            messages.error(request, "You don't have permission to view bills.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = Bill.objects.all().select_related('table', 'order', 'cashier')
        
        # Filter by status if provided
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-generated_at')


class BillGenerateView(LoginRequiredMixin, View):
    """Generate bill for a table"""
    template_name = 'billing/bill_generate.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_cashier or request.user.is_manager):
            messages.error(request, "You don't have permission to generate bills.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        # Get tables with served orders that don't have bills
        orders_needing_bills = Order.objects.filter(
            status=Order.Status.SERVED,
            bill__isnull=True
        ).select_related('table', 'waiter')
        
        context = {
            'orders_needing_bills': orders_needing_bills,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        order_id = request.POST.get('order_id')
        
        try:
            order = Order.objects.get(id=order_id, status=Order.Status.SERVED, bill__isnull=True)
            
            with transaction.atomic():
                # Calculate bill amounts
                from decimal import Decimal
                subtotal = order.calculate_total()
                tax_percentage = Decimal('5.00')  # Default 5% tax
                tax_amount = (subtotal * tax_percentage) / Decimal('100.00')
                total_amount = subtotal + tax_amount
                
                # Create bill with all required fields
                bill = Bill.objects.create(
                    table=order.table,
                    order=order,
                    cashier=request.user,
                    subtotal=subtotal,
                    tax_percentage=tax_percentage,
                    tax_amount=tax_amount,
                    total_amount=total_amount,
                )
            
            messages.success(request, f"Bill generated successfully for {order.table}")
            return redirect('billing:detail', pk=bill.pk)
        
        except Order.DoesNotExist:
            messages.error(request, "Order not found or already has a bill")
            return redirect('billing:generate')


class BillDetailView(LoginRequiredMixin, DetailView):
    """View bill details"""
    model = Bill
    template_name = 'billing/bill_detail.html'
    context_object_name = 'bill'
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_cashier or request.user.is_manager):
            messages.error(request, "You don't have permission to view bills.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)


class BillPaymentView(LoginRequiredMixin, View):
    """Process bill payment"""
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_cashier or request.user.is_manager):
            messages.error(request, "You don't have permission to process payments.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, pk):
        bill = get_object_or_404(Bill, pk=pk)
        
        if bill.status == Bill.Status.PAID:
            messages.warning(request, "This bill is already paid")
        else:
            bill.mark_as_paid(cashier=request.user)
            messages.success(request, f"Payment processed successfully for {bill.table}. Table is now available.")
        
        return redirect('billing:detail', pk=bill.pk)


class BillPDFExportView(LoginRequiredMixin, View):
    """Export bill as PDF"""
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_cashier or request.user.is_manager):
            messages.error(request, "You don't have permission to export bills.")
            return redirect('dashboard:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, pk):
        bill = get_object_or_404(Bill, pk=pk)
        
        # Generate PDF
        pdf_buffer = bill.export_to_pdf()
        
        # Return as download
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="bill_{bill.pk}_{bill.table.table_number}.pdf"'
        
        return response
