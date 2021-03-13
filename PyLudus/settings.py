"""
Django settings for PyLudus project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import pathlib
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG") == "true"
print(f"{DEBUG=}")

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "127.0.0.1")
if "," in ALLOWED_HOSTS:
    ALLOWED_HOSTS = ALLOWED_HOSTS.split(",")
else:
    ALLOWED_HOSTS = [ALLOWED_HOSTS]
print(f"{ALLOWED_HOSTS}")


# LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = os.environ.get("LOGIN_REDIRECT_URL", "http://127.0.0.1:8000")
# LOGOUT_REDIRECT_URL = 'home'


# Fusion auth Keys
# Note store this outside the settings page later and pull it in from another file
# NOTE: SECURE_SSL_REDIRECT does not work correctly :(
# SECURE_SSL_REDIRECT = True if os.environ.get('SECURE_SSL_REDIRECT')=='true' else False
FUSION_AUTH_APP_ID = os.environ.get("FUSION_AUTH_APP_ID")
FUSION_AUTH_CLIENT_SECRET = os.environ.get("FUSION_AUTH_CLIENT_SECRET")
FUSION_AUTH_API_KEY = os.environ.get("FUSION_AUTH_API_KEY")
FUSION_AUTH_BASE_URL = os.environ.get("FUSION_AUTH_BASE_URL")
FUSION_AUTH_INTERNAL_API_URL = os.environ.get("FUSION_AUTH_INTERNAL_API_URL")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "PyLudus.apps.home",
    "widget_tweaks",
    "bootstrap4",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Do not replace the below line in new project being created.
ROOT_URLCONF = "PyLudus.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "PyLudus", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Do not replace the below line in new project being created.
WSGI_APPLICATION = "PyLudus.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        # Note that I have changed this because of an error on the built in line
        # Probably only a windows issue here.
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s | %(process)d:%(thread)d | %(module)s | %(levelname)-8s | %(message)s'
            )
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': os.environ.get(
                'LOG_LEVEL',
                # If there is no explicit `LOG_LEVEL` set,
                # use `DEBUG` if we're running in debug mode
                # Use `ERROR` if we're not running in debug mode
                'INFO' if DEBUG else 'ERROR'
            )
        }
    }
}