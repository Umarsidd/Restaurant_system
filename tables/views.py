from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Table


class TableListView(LoginRequiredMixin, ListView):
    """List all tables"""
    model = Table
    template_name = 'tables/table_list.html'
    context_object_name = 'tables'
    
    def get_queryset(self):
        return Table.objects.all().order_by('table_number')


class TableCreateView(LoginRequiredMixin, CreateView):
    """Create a new table (Manager only)"""
    model = Table
    template_name = 'tables/table_form.html'
    fields = ['table_number', 'seating_capacity', 'status']
    success_url = reverse_lazy('tables:list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            messages.error(request, "Only managers can create tables.")
            return redirect('tables:list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f"Table {form.instance.table_number} created successfully")
        return super().form_valid(form)


class TableUpdateView(LoginRequiredMixin, UpdateView):
    """Update a table (Manager only)"""
    model = Table
    template_name = 'tables/table_form.html'
    fields = ['table_number', 'seating_capacity', 'status']
    success_url = reverse_lazy('tables:list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            messages.error(request, "Only managers can edit tables.")
            return redirect('tables:list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f"Table {form.instance.table_number} updated successfully")
        return super().form_valid(form)


class TableDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a table (Manager only)"""
    model = Table
    template_name = 'tables/table_confirm_delete.html'
    success_url = reverse_lazy('tables:list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            messages.error(request, "Only managers can delete tables.")
            return redirect('tables:list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f"Table {self.object.table_number} deleted successfully")
        return super().form_valid(form)
