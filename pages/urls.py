# Django Built-in modules
from django.urls import path
# Local apps
from . import views

app_name = 'pages'

urlpatterns = [
    path('home/', views.HomePageDetailView.as_view(), name='home'),
    path('about-us/', views.AboutPageDetailView.as_view(), name='about_us'),

]
