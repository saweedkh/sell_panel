"""
URL configuration for sell_panel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Django Built-in modules
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
# Third Party Packages
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


api_v1_urlpatterns = [
    # Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Account
    path('account/', include('account.urls', namespace='account')),
    # Pages
    path('pages/', include('pages.urls', namespace='pages')),
    # Blog
    path('blog/', include('blog.urls', namespace='blog')),
    # Contact Us
    path('contact-us/', include('contact_us.urls', namespace='contact_us')),
    # Article
    path('article/', include('article.urls', namespace='article')),
    # Newsletter
    path('newsletters/', include('newsletters.urls', namespace='newsletters')),
    # Products
    path('products/', include('products.urls', namespace='products')),
    # Setting
    path('setting/', include('setting.urls', namespace='setting')),
    # Areas
    path('area/', include('area.urls', namespace='area')),
    # Captcha
    path('captcha/', include('captcha.urls')),
    

]

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),

    # # Site Map
    # path('sitemap.xml', views.index, {'sitemaps': sitemaps}),
    # path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # Third party
    path('__debug__/', include('debug_toolbar.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    path('api/v1/', include(api_v1_urlpatterns)),

]

urlpatterns += i18n_patterns(
    path('admin/dynamic_raw_id/', include('dynamic_raw_id.urls')),
    # Admin panel
    path('admin/', admin.site.urls),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
