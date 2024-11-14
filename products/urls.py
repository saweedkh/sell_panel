# Django Built-in modules
from django.urls import path
from django.conf import settings
from django.views.decorators.cache import cache_page

# Locals apps
from . import views

# Third Party Packages
import mptt_urls

app_name = 'products'

CACHE_TTL = getattr(settings, 'CACHE_TTL', settings.DEFAULT_TIMEOUT)

urlpatterns = [
    path('', cache_page(CACHE_TTL)(views.ProductView.as_view()), name='product-list'),
    path('<id>/', cache_page(CACHE_TTL)(views.ProductDetailView.as_view()), name='product-detail'),
    path('reply_comment/', cache_page(CACHE_TTL)(views.ProductCommentAPIView.as_view()), name = 'product-reply-comment'),
]
