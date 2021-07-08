"""
Django settings for intranetPoli project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import json
import os
from datetime import datetime

from django.contrib.messages import constants as messages
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'secret.json')) as secret_file:
    _secrets = json.load(secret_file)


def get_secret(configuracao, banco=None, secrets=_secrets):
    """
    Obtêm a configuração secreta ou eleva um "ImproperlyConfigured" erro

    :param configuracao:
    :param secrets:
    :return:
    """
    try:
        return secrets[configuracao.upper()] if banco is None else secrets['DB'][banco.upper()][configuracao.upper()]
    except KeyError:
        msg = f"Não existe a configuração: '{configuracao}'"
        raise ImproperlyConfigured(msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if get_secret("DEBUG") == 'True' else False

ALLOWED_HOSTS = get_secret("HOSTS")

# Application definition

INSTALLED_APPS = [
    'Apps.intranet',
    'Apps.subsTribut',
    'Apps.assinaturas',
    'Apps.catalogos',
    'Apps.resultadoContabil',
    'widget_tweaks',
    'simple_history',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'intranetPoli.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'intranetPoli.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': get_secret('DB_NAME', banco='default'),
        'USER': get_secret('DB_USER', banco='default'),
        'PASSWORD': get_secret('DB_PASSWORD', banco='default'),
        'HOST': '',
        'PORT': '',
    },
    'BI': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': get_secret('DB_NAME', banco='bi'),
        'USER': get_secret('DB_USER', banco='bi'),
        'PASSWORD': get_secret('DB_PASSWORD', banco='bi'),
        'HOST': '',
        'PORT': '',
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# STATICS
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'intranetPoli/static')
]
# MEDIA
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# MESSAGES
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
}

# LOGIN
LOGIN_URL = 'login'

# LOGGING
if get_secret("LOGGING") == 'True':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                f'level': {get_secret('LOGGING_LEVEL')},
                'class': 'logging.FileHandler',
                f'filename': os.path.join(BASE_DIR, "logs", f'log-{datetime.now().date()}'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
