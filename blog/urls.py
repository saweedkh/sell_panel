# Django Built-in modules
from django.urls import path

# Locals apps
from . import views

app_name = 'blog'

urlpatterns = [
    # admin
    path('automate_description/', views.automate_description, name='automate_description'),
    #
    # path('posts/', views.PostListView.as_view(), name='posts'),
    # path('post/<slug>/', views.PostDetailView.as_view(), name='post'),
    # path('categories/', views.CategoryListView.as_view(), name='categories'),
    # path('category/<slug>/', views.CategoryDetailView.as_view(), name='category'),
]
