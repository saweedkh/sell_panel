# Django Built-in modules
from django.urls import path

from . import views

app_name = 'notification'

urlpatterns = [
   
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', views.DetailNotificationView.as_view(), name='notification-detail'),
    path('read/<int:pk>/', views.ReadNotificationView.as_view(), name='read-notification'),
    
]