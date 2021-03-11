"""
Django settings for purpleserver project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import importlib
from pathlib import Path
from decouple import config
from django.urls import reverse_lazy
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG_MODE', default=True, cast=bool)

# custom env
WORK_DIR = config('WORK_DIR', default='')
Path(WORK_DIR).mkdir(parents=True, exist_ok=True)

USE_HTTPS = config('USE_HTTPS', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')
CORS_ORIGIN_ALLOW_ALL = True

with open(BASE_DIR / 'purpleserver' / 'VERSION', "r") as v:
    VERSION = v.read()

# HTTPS configuration
if USE_HTTPS is True:
    global SECURE_SSL_REDIRECT
    global SECURE_PROXY_SSL_HEADER
    global SESSION_COOKIE_SECURE
    global SECURE_HSTS_SECONDS
    global SECURE_HSTS_INCLUDE_SUBDOMAINS
    global CSRF_COOKIE_SECURE
    global SECURE_HSTS_PRELOAD

    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 1
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_PRELOAD = True


# Application definition

PURPLSHIP_CONF = [
    app for app in [
        {'app': 'purpleserver.core', 'module': 'purpleserver.core', 'urls': 'purpleserver.core.urls'},
        {'app': 'purpleserver.providers', 'module': 'purpleserver.providers', 'urls': 'purpleserver.providers.urls'},
        {'app': 'purpleserver.proxy', 'module': 'purpleserver.proxy', 'urls': 'purpleserver.proxy.urls'},
        {'app': 'purpleserver.manager', 'module': 'purpleserver.manager', 'urls': 'purpleserver.manager.urls'},
        {'app': 'purpleserver.events', 'module': 'purpleserver.events', 'urls': 'purpleserver.events.urls'},
        {'app': 'purpleserver.client', 'module': 'purpleserver.client', 'urls': 'purpleserver.client.urls'},
        {'app': 'purpleserver.pricing', 'module': 'purpleserver.pricing'},
    ]
    if importlib.util.find_spec(app['module']) is not None
]

PURPLSHIP_APPS = [cfg['app'] for cfg in PURPLSHIP_CONF]
PURPLSHIP_URLS = [cfg['urls'] for cfg in PURPLSHIP_CONF if 'urls' in cfg]


BASE_APPS = [
    'purpleserver.user',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

INSTALLED_APPS = [
    'constance',

    *PURPLSHIP_APPS,
    *BASE_APPS,

    'rest_framework',
    'rest_framework.authtoken',

    'django_email_verification',
    'rest_framework_tracking',

    'drf_yasg',
    'constance.backends.database',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'purpleserver.urls'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
OPEN_API_PATH = 'api/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'purpleserver' / 'templates'
        ],
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

WSGI_APPLICATION = 'purpleserver.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DB_ENGINE = config('DATABASE_ENGINE', default='postgresql_psycopg2')

DATABASES = {
    'default': {
        'NAME': config('DATABASE_NAME', default='db'),
        'ENGINE': 'django.db.backends.{}'.format(DB_ENGINE),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'USER': config('DATABASE_USERNAME', default=''),
        'HOST': config('DATABASE_HOST', default=''),
        'PORT': config('DATABASE_PORT', default=''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
AUTH_USER_MODEL = 'user.User'


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'purpleserver' / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'purpleserver' / 'static'
]


# Django REST framework

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),

    'DEFAULT_THROTTLE_RATES': {
        'anon': '40/minute',
        'user': '60/minute'
    },

    'EXCEPTION_HANDLER': 'purpleserver.core.exceptions.custom_exception_handler',

    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },

    'TEST_REQUEST_DEFAULT_FORMAT': 'json',

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}


# OpenAPI config

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'LOGIN_URL': reverse_lazy('admin:login'),
    'LOGOUT_URL': '/admin/logout',

    'DEFAULT_INFO': 'purpleserver.urls.swagger_info',

    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    },
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
    'HIDE_HOSTNAME': True,
    'REQUIRED_PROPS_FIRST': True,
}

# Logging configuration

LOG_LEVEL = ('DEBUG' if DEBUG else config('LOG_LEVEL', default='INFO'))
DJANGO_LOG_LEVEL = ('INFO' if DEBUG else config('DJANGO_LOG_LEVEL', default='WARNING'))
LOG_FILE_DIR = config('LOG_DIR', default=WORK_DIR)
LOG_FILE_NAME = os.path.join(LOG_FILE_DIR, 'debug.log')
DRF_TRACKING_ADMIN_LOG_READONLY = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': LOG_FILE_NAME,
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': DJANGO_LOG_LEVEL,
            'propagate': False,
        },
        'purplship': {
            'handlers': ['file', 'console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
        'purpleserver': {
            'handlers': ['file', 'console'],
            'level': LOG_LEVEL,
            'propagate': False,
        },
    },
}

# Purplship Server Background jobs interval config
DEFAULT_SCHEDULER_RUN_INTERVAL = 3600  # value is seconds. so 3600 seconds = 1 Hour
DEFAULT_TRACKERS_UPDATE_INTERVAL = 10800  # value is seconds. so 10800 seconds = 3 Hours
