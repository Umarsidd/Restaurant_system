from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='home'),
    path('table-status/', views.TableStatusDashboardView.as_view(), name='table_status'),
    path('waiter/', views.WaiterDashboardView.as_view(), name='waiter'),
    path('cashier/', views.CashierDashboardView.as_view(), name='cashier'),
    path('manager/', views.ManagerDashboardView.as_view(), name='manager'),
]
