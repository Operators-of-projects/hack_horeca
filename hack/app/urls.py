from django.urls import path
from rest_framework import routers

from . import views


urlpatterns = [
    path('create-client/', views.AddClientView.as_view()),
    path('create-vendor/', views.AddVendorView.as_view()),
    path('vendors/', views.GetVendersView.as_view()),
    path('client/<int:client_id>/', views.DetailClientView.as_view()),
    path('vendor/<int:vendor_id>/', views.DetailVendorView.as_view()),
    path('create-product/', views.CreateProductView.as_view()),
    path('product/<int:product_id>/', views.DetailProductView.as_view()),
    path('vendor/<int:vendor_id>/products/', views.ProductsView.as_view()),
    path('vendor/<int:vendor_id>/transactions/', views.VendorTransactionView.as_view()),
    path('vendor/<int:vendor_id>/gps/', views.GetClientsByGPSView.as_view()),
    path('client/<int:client_id>/transactions/', views.ClientTransactionView.as_view()),
    path('transaction/<int:transaction_id>/', views.DetailTransactionView.as_view()),
    path('transaction/<int:transaction_id>/report/', views.AddReportToTransactionView.as_view()),
]
