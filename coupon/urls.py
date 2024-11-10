# Django Built-in modules
from django.urls import path

# Locals apps
from . import views

app_name = 'coupon'

urlpatterns = [
    path('generate-code-ajax/', views.generate_discount_coupon, name='generate_code')
]
