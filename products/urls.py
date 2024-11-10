# Django Built-in modules
from django.urls import path
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page

# Locals apps
from . import views

# Third Party Packages
import mptt_urls

app_name = 'products'

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

urlpatterns = [
    path('', cache_page(CACHE_TTL)(views.ProductView.as_view()), name='product-list'),
    path('category/', cache_page(CACHE_TTL)(views.CategoryListView.as_view()), name='category-list'),
    path('<id>/', cache_page(CACHE_TTL)(views.ProductDetailView.as_view()), name='product-detail'),
    path('reply_comment/', cache_page(CACHE_TTL)(views.ProductCommentAPIView.as_view()), name = 'product-reply-comment'),
]
