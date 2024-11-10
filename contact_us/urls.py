# Django Built-in modules
from django.urls import path

# Local Apps
from . import views

app_name = 'contact-us'

urlpatterns = [
    path('submit-message/', views.ContactUsMessageCreateView.as_view(), name='submit-message'),
    path('contact-ways/', views.ContactUsDetailView.as_view(), name='submit-message'),
]
