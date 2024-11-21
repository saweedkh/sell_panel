"""
Django settings for sell_panel project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from datetime import timedelta
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yevfh&1rt=-5bx9!b7#ox9#z&9r6gn&)-84%i(o1c1)f69k$2o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_DOMAIN = '127.0.0.1'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'admin_interface',  # Third Party
    'modeltranslation',  # Third Party
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local apps
    'products', 
    'orders',
    'payment',
    'account',
    'area',
    'article',
    'blog',
    'setting',
    'category',
    'coupon',
    'contact_us',
    'gateways',
    'menu',
    'newsletters',
    'pages',
    'seo',
    'utils',
    'translator',
    'smart_selects',
    'autosave',
    'notification',
    
    
    # Third Party Apps
    'debug_toolbar',
    'mptt',
    'imagekit',
    'ckeditor',
    'ckeditor_uploader',
    'auditlog',
    'colorfield',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'django_filters',
    'jalali_date',
    'corsheaders',
    'dynamic_raw_id',
    'adminsortable2',
    'captcha',
    'django_json_widget',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # corsheaders
    "corsheaders.middleware.CorsMiddleware",
    # Default Language Middleware
    'utils.middlewares.DefaultLanguageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Django Debug Toolbar Middleware
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # Redirect Middleware
    'utils.middlewares.RedirectToNonWww',
    # Django Locale Middleware
    'django.middleware.locale.LocaleMiddleware',
    # Third Party Packages
    'auditlog.middleware.AuditlogMiddleware',
]

ROOT_URLCONF = 'sell_panel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sell_panel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
     'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sell_panel',
        'USER': 'root',
        'PASSWORD': 'vt9wiJxn0ruIxTtGiOls1pry',
        'HOST': 'database',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'fa'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
]


MODELTRANSLATION_DEFAULT_LANGUAGE = 'fa'

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    'static/',
]

STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# AUTHENTICATION USER MODEL
AUTH_USER_MODEL = 'account.User'

# Django auditlog
AUDITLOG_INCLUDE_ALL_MODELS = True
AUDITLOG_DISABLE_ON_RAW_SAVE = False
AUDITLOG_EXCLUDE_TRACKING_MODELS = ()

# Django Admin Interface  Configurations
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]


# CKEditor  Configurations
CKEDITOR_BASEPATH = f"{STATIC_URL}ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_RESTRICT_BY_DATE = True
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_THUMBNAIL_SIZE = (800, 600)
CKEDITOR_IMAGE_QUALITY = 70
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'office2013',
        'toolbar': 'full',
        'width': 'full',
        'extraPlugins': ','.join(['html5video', ]),
    },
    'basic': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ]
    }
}

# DRF configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Global Configure anomalous module
    'EXCEPTION_HANDLER': 'utils.exception.custom_exception_handler',
    # Modify the default return JSON's renderer class
    'DEFAULT_RENDERER_CLASSES': (
        'utils.rendererresponse.customrenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'utils.paginator.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Sell Panel',
    'DESCRIPTION': 'Sell Panel API Schema',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
}

# Multi Languages Fields Render
USE_MULTI_LANGUAGE_FIELDS = False

RECAPTCHA_PUBLIC_KEY = '6LfKYJIoAAAAAEPO7ESGCsDDW1eSYfD5C5ucs4El'
RECAPTCHA_PRIVATE_KEY = '6LfKYJIoAAAAAOsL_PmkjrQyZBf1E21C9xbLYtKg'

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_LENGTH = 5
CAPTCHA_NOISE_FUNCTIONS = ()
CAPTCHA_LETTER_ROTATION = (-10, 10)


# Cache Timeout
DEFAULT_TIMEOUT = 3600

# phone number settings
PHONENUMBER_DEFAULT_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'IR'

# Override Local Setting
try:
    if os.environ.get('DJANGO_DEVELOPMENT'):
        from sell_panel.local_settings import *
except ModuleNotFoundError:
    pass


