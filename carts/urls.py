# Django Built-in modules
from django.urls import path

# Locals apps
from . import views

app_name = 'carts'

urlpatterns = [
    path('', views.show, name='show'),
    path('add/', views.add, name='cart_add'),
    path('remove/', views.remove, name='cart_remove'),
    path('set_quantity/', views.set_quantity, name='set_quantity'),
    path('apply_discount_coupon/', views.apply_discount_coupon, name='apply_discount_coupon'),
    path('remove_discount_coupon/', views.remove_discount_coupon, name='remove_discount_coupon'),
    path('add-shipment/', views.add_shipment, name='add_shipment'),
    path('add-payment/', views.add_payment, name='add_payment'),
    path('load-cart-menu/', views.load_cart_menu, name='load_cart_menu'),
]
