"""
Django settings for config project — Palace Karimi B2B Export.

Production-hardened configuration.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')


# ==============================================================================
# Security — Must be set before anything else reads them
# ==============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '')

if not SECRET_KEY:
    if os.environ.get('DEBUG', 'False').lower() == 'true':
        SECRET_KEY = 'django-insecure-dev-mode-only-!!change-me!!'
    else:
        raise RuntimeError(
            'SECRET_KEY environment variable is not set. '
            'Refusing to start in production without a valid key.'
        )

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS
_allowed_hosts_raw = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [h.strip() for h in _allowed_hosts_raw.split(',') if h.strip()] if _allowed_hosts_raw else []

# CSRF_TRUSTED_ORIGINS — required when behind a reverse proxy / CDN
_csrf_raw = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_raw.split(',') if o.strip()] if _csrf_raw else []

# SECURE_PROXY_SSL_HEADER — tells Django to trust X-Forwarded-Proto from Nginx
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Security hardening — always on
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

# HTTPS-dependent security — only enable when SSL is actually configured
USE_HTTPS = os.environ.get('USE_HTTPS', 'False').lower() == 'true'

if USE_HTTPS:
    SECURE_HSTS_SECONDS = 31536000          # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False


# ==============================================================================
# Application definition
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # Third-party apps
    'parler',
    'rosetta',

    # Local apps
    'core',
    'catalog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.PermissionsPolicyMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ==============================================================================
# Database
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'palace_db'),
        'USER': os.environ.get('DB_USER', 'palace_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}


# ==============================================================================
# Password validation
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==============================================================================
# Internationalization / RTL / Multilingual
# ==============================================================================

LANGUAGE_CODE = 'fa-IR'
TIME_ZONE = 'Asia/Tehran'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('fa', _('Persian')),
    ('en', _('English')),
    ('ar', _('Arabic')),
    ('tr', _('Turkish')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

SITE_ID = 1

PARLER_LANGUAGES = {
    SITE_ID: (
        {'code': 'fa'},
        {'code': 'en'},
        {'code': 'ar'},
        {'code': 'tr'},
    ),
    'default': {
        'fallback': 'fa',
        'hide_untranslated': False,
    },
}


# ==============================================================================
# Static & media files
# ==============================================================================

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# Logging — Docker-friendly stdout/stderr
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s | %(levelname)-8s | %(name)s | '
                '%(funcName)s:%(lineno)d | %(message)s'
            ),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s | %(levelname)-8s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
        'stderr': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stderr,
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['stderr'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['stderr'],
            'level': 'WARNING',
            'propagate': False,
        },
        'catalog': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ==============================================================================
# Cache — PostgreSQL-backed cache for django-ratelimit
# ==============================================================================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "rate_limit_cache",
        "TIMEOUT": 3600,
        "OPTIONS": {
            "MAX_ENTRIES": 10000,
        },
    }
}