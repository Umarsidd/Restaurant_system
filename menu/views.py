from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

from .models import MenuItem


class MenuItemListView(LoginRequiredMixin, ListView):
    """List all menu items"""
    model = MenuItem
    template_name = 'menu/menu_list.html'
    context_object_name = 'menu_items'
    
    def get_queryset(self):
        queryset = MenuItem.objects.all().order_by('category', 'name')
        
        # Filter by category if provided
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by availability if not manager
        if not self.request.user.is_manager:
            queryset = queryset.filter(is_available=True)
        
        return queryset


class MenuItemCreateView(LoginRequiredMixin, CreateView):
    """Create a new menu item (Manager only)"""
    model = MenuItem
    template_name = 'menu/menu_form.html'
    fields = ['name', 'category', 'price', 'description', 'image', 'is_available']
    success_url = reverse_lazy('menu:list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            messages.error(request, "Only managers can create menu items.")
            return redirect('menu:list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f"Menu item '{form.instance.name}' created successfully")
        return super().form_valid(form)


class MenuItemUpdateView(LoginRequiredMixin, UpdateView):
    """Update a menu item (Manager only)"""
    model = MenuItem
    template_name = 'menu/menu_form.html'
    fields = ['name', 'category', 'price', 'description', 'image', 'is_available']
    success_url = reverse_lazy('menu:list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            messages.error(request, "Only managers can edit menu items.")
            return redirect('menu:list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f"Menu item '{form.instance.name}' updated successfully")
        return super().form_valid(form)


class MenuItemDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a menu item (Manager only)"""
    model = MenuItem
    template_name = 'menu/menu_confirm_delete.html'
    success_url = reverse_lazy('menu:list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            messages.error(request, "Only managers can delete menu items.")
            return redirect('menu:list')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, f"Menu item '{self.object.name}' deleted successfully")
        return super().form_valid(form)


class MenuItemToggleAvailabilityView(LoginRequiredMixin, View):
    """Toggle menu item availability (Manager only)"""
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_manager:
            messages.error(request, "Only managers can toggle availability.")
            return redirect('menu:list')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, pk):
        menu_item = MenuItem.objects.get(pk=pk)
        menu_item.toggle_availability()
        
        status = "available" if menu_item.is_available else "unavailable"
        messages.success(request, f"'{menu_item.name}' is now {status}")
        
        return redirect('menu:list')
