# Django Build-in
from django.urls import path

# Local Apps
from . import views

app_name = 'setting'

urlpatterns = [
    path('', views.GlobalSettingDetailView.as_view(), name='global-settings'),
]
