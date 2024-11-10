from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('billing/', views.billing, name='billing'),
    path('order-tracking/', views.tracking, name='tracking'),
    path('invoice/<invoice_id>/', views.invoice, name='invoice'),
    path('thermal-printer-invoice/<invoice_id>/', views.thermal_printer_invoice, name='thermal_printer_invoice'),
    path('create_invoice/<order_id>/', views.create_invoice, name='create_invoice'),
    path('review/<order_uuid>/', views.order_review, name="order_review"),
    
    path('create/', views.CreateOrderView.as_view(), name='create_order'),
    path('list/', views.OrderListView.as_view(), name='order_list'),
    path('detail/<tracking_code>/', views.OrderDetailView.as_view(), name='order_detail'),
]
