# Django Build-in
from django.urls import path

# Local Apps
from . import views

app_name = 'terms-and-faqs'

urlpatterns = [
    path('faq/categories/', views.FAQCategoryListView.as_view(), name='faq-categories'),
    path('faq/list/', views.FAQListView.as_view(), name='faq-list'),
    path('terms/categories/', views.TermsCategoryListView.as_view(), name='terms-categories'),
    path('terms/list/', views.TermsItemsListView.as_view(), name='terms-list'),
]
