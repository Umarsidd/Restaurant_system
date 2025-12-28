from django.urls import path
from . import views

app_name = 'tables'

urlpatterns = [
    path('', views.TableListView.as_view(), name='list'),
    path('create/', views.TableCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TableUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.TableDeleteView.as_view(), name='delete'),
]
