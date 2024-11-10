# Django Built-in modules
from django.urls import path

# Locals apps
from . import views

app_name = 'menu'

urlpatterns = [
    path('gfk-lookup-ajax/', views.gfk_lookup, name='gfk_lookup_ajax')
]
