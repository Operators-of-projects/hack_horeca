from django.urls import path
from rest_framework import routers

from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('orders/', views.orders, name='orders'),
    path('products/', views.products, name='products'),
    path('create-client/', views.AddClientView.as_view()),
    path('create-vendor/', views.AddVendorView.as_view()),
    path('create-transaction/', views.AddTransaction.as_view()),
    path('vendors/', views.GetVendersView.as_view()),
    path('client/<int:client_id>/', views.DetailClientView.as_view()),
    path('clients/', views.GetClientsView.as_view()),
    path('vendor/<int:vendor_id>/', views.DetailVendorView.as_view()),
    path('create-product/', views.CreateProductView.as_view()),
    path('product/<int:product_id>/', views.DetailProductView.as_view()),
    path('vendor/<int:vendor_id>/products/', views.ProductsView.as_view()),
    path('vendor/<int:vendor_id>/created/', views.NewTransactionsView.as_view()),
    path('vendor/<int:vendor_id>/not-done/', views.GetNewOrViewedTransactionView.as_view()),
    path('vendor/<int:vendor_id>/transactions/', views.VendorTransactionView.as_view()),
    path('vendor/<int:vendor_id>/gps/', views.GetClientsByGPSView.as_view()),
    path('client/<int:client_id>/transactions/', views.ClientTransactionView.as_view()),
    path('transaction/<int:transaction_id>/', views.DetailTransactionView.as_view()),
    path('transaction/<int:transaction_id>/report/', views.AddReportToTransactionView.as_view()),
    path('transaction/<int:transaction_id>/qrcode/', views.GenerateQRView.as_view()),
]
