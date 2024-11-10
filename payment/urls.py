# Django Built-in modules
from django.urls import path
# Local apps
from . import views

app_name = 'payment'

urlpatterns = [
    # path('payment-order/<tracking_code>/', views.payment_order, name='payment_order'),
    path('transaction/', views.callback_gateway, name='callback_gateway'),
    path('bank-receipt/<tracking_code>/', views.upload_bank_receipt, name='upload_bank_receipt'),
    path('withdraw_from_wallet/<tracking_code>/', views.withdraw_from_wallet, name='withdraw_from_wallet'),
    path('post_paid_payment/<tracking_code>/', views.post_paid_payment, name='post_paid_payment'),
    path('success/<tracking_code>/<order_uuid>/', views.success_result, name='success'),
    path('failed/<tracking_code>/<order_uuid>/', views.failed_result, name='failed'),
    path('exception/<tracking_code>/<order_uuid>/', views.exception, name='exception'),
    
    
    path('payment-order/<tracking_code>/', views.PaymentOrder.as_view(), name='payment_order'),
    path('invoice/', views.GetInvoiceView.as_view(), name='get_invoice'),
    path('payment-order/<tracking_code>/', views.payment_invoice, name='payment_invoice'),
]
