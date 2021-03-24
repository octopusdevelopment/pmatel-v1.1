"""
Django settings for pmatel project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from django.contrib.messages import constants as messages
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE')
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE')
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'coupons.apps.CouponsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'ckeditor',
    'ckeditor_uploader',
    'debug_toolbar',
    # 'ckeditor_uploader', ## pour les fichiers static
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pmatel.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.category',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'pmatel.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

AUTHENTICATION_BACKENDS = (
    ('django.contrib.auth.backends.ModelBackend'),
)

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'fr'

TIME_ZONE = 'Africa/Algiers'

USE_I18N = True

USE_L10N = True

USE_TZ = True



CKEDITOR_CONFIGS = {
    'default':
        {
            'skin': 'moono',
            'toolbar': 'full', 
            "removePlugins": "stylesheetparser",
            'toolbar_Custom': [
                ['Bold', 'Link', 'Unlink', 'Image'], 
            ], 
            'extraPlugins': ','.join(['codesnippet']),
}}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
    ]


STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
CKEDITOR_UPLOAD_PATH = 'uploads/'
MEDIA_URL ='/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

INTERNAL_IPS = ['127.0.0.1', '::1', '0.0.0.0']

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'primary'

}

CART_SESSION_ID = 'cart'


# EMAIL CONFIGURATION -- TODO: change later

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'Hildweig@gmail.com'
EMAIL_HOST_PASSWORD = 'euevnbkbghiutshv'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
