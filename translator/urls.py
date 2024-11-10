from django.urls import path
from . import views

app_name = 'translator'

urlpatterns = [
    path('', views.TranslatorView.as_view(), name='translating'),
    # path('', views.translator_view, name='translating'),
]
