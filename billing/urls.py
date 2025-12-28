from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('', views.BillListView.as_view(), name='list'),
    path('generate/', views.BillGenerateView.as_view(), name='generate'),
    path('<int:pk>/', views.BillDetailView.as_view(), name='detail'),
    path('<int:pk>/pay/', views.BillPaymentView.as_view(), name='pay'),
    path('<int:pk>/pdf/', views.BillPDFExportView.as_view(), name='pdf'),
]
