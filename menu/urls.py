from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.MenuItemListView.as_view(), name='list'),
    path('create/', views.MenuItemCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.MenuItemUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.MenuItemDeleteView.as_view(), name='delete'),
    path('<int:pk>/toggle/', views.MenuItemToggleAvailabilityView.as_view(), name='toggle'),
]
