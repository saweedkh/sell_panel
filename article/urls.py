# Django Build-in
from django.urls import path

# Local Apps
from . import views

app_name = 'article'

urlpatterns = [
    path('tags/', views.TagListView.as_view(), name='tags'),
    path('', views.ArticlePostListView.as_view(), name='posts'),
    path('<id>/', views.ArticlePostDetailView.as_view(), name='post'),
    path('create/comment/', views.ArticleCommentsCreateView.as_view(), name='create-comment'),
    path('create/like/', views.ArticleCommentLikesCreateView.as_view(), name='create-like'),
    path('posts/categories/', views.CategoryListView.as_view(), name='categories'),
    path('posts/category/<id>/', views.CategoryDetailView.as_view(), name='category'),
]
