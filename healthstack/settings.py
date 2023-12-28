"""
Django settings for healthstack project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from django.core.management.utils import get_random_secret_key
get_random_secret_key()

import os
import environ
# django-environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

### setting up env
env = environ.Env()

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your_secret_key_value'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # or DEBUG = False


ALLOWED_HOSTS = ['192.168.0.100', '127.0.0.1','5749-103-109-53-5.in.ngrok.io']
# ALLOWED_HOSTS = ['mobile view', 'local host','ngrok -- keeps on changing']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hospital.apps.HospitalConfig',
    'hospital_admin.apps.HospitalAdminConfig',
    'doctor.apps.DoctorConfig',
    'pharmacy.apps.PharmacyConfig',
    'sslcommerz.apps.SslcommerzConfig',
    'widget_tweaks',
    'rest_framework',
    'ChatApp.apps.ChatappConfig',
    'debug_toolbar',
 

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = 'healthstack.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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

WSGI_APPLICATION = 'healthstack.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kathmandu'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/images/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# settings.py



# stripe ------------------------------------->
STRIPE_PUBLISHABLE_KEY = 'pk_test_51NSvk2JME8kW2R5KxJ0lZuygJ6kRAXbVfVT3Bl4ik9stYGrF2LLziBoJQ2o1bScl7JGv85r5tXLSxoJi6Q2PaWXT00icCrvjTW'
STRIPE_SECRET_KEY = 'sk_test_51NSvk2JME8kW2R5KbvcGRjAMi2MPHEr5QsjJnx5s7FpN2dGYGDPR1PTfyHDaWD9EGfUEjeNgNc9XRxrYyrPed2U300RZYaO0RH'


### SSLCOMMERZ env variables
#VARIABLE should be in capital letter.
STORE_ID = 'your_store_id'
STORE_PASSWORD = 'your_store_password'
STORE_NAME = 'your_store_name'


###Mailtrap env Variables
SMTP_HOST = 'your_smtp_host'

SMTP_PORT = 'your_smtp_port'
SMTP_USER = 'your_smtp_user'
SMTP_PASSWORD = 'your_smtp_password'

# EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailtrap.io'
EMAIL_PORT = SMTP_PORT
EMAIL_HOST_USER = SMTP_USER
EMAIL_HOST_PASSWORD = SMTP_PASSWORD
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False



# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'hospital.User'


# SESSION AGE 45 Minutes
SESSION_COOKIE_AGE = 45*60
SESSION_SAVE_EVERY_REQUEST = True