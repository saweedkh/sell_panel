# Django Built-in modules
from django.urls import path

# Local Apps
from . import views

app_name = 'newsletters'

urlpatterns = [
    path('member/create/', views.MemberCreateView.as_view(), name='newsletters_create_member'),
]
