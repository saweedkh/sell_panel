# Django Built-in modules
from django.urls import path, include

# Local Apps
from . import views

app_name = 'areas'

urlpatterns = [
    path('province/list/', views.ProvinceListView.as_view(), name='province_list'),
    path('city/list/', views.CityListView.as_view(), name='city_list'),
]
