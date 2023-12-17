"""
Django settings for shuaibb project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from corsheaders.defaults import (
    default_headers,
    default_methods
)
from dotenv import load_dotenv, dotenv_values

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_BASE_DIR = Path(BASE_DIR.parent)
ENV_CONFIG = {
    **dotenv_values(ENV_BASE_DIR / '.env')
}

env = ENV_CONFIG.get('ENV', 'dev') 

if (os.getenv('ENV') is not None):
    env = os.getenv('ENV')


is_test_or_prod = (env == 'test' or env == 'prod')

ENV_CONFIG = {
    **ENV_CONFIG,
    **dotenv_values(ENV_BASE_DIR / ".env.{override}".format(override=env))
}
# Build paths inside the project like this: BASE_DIR / 'subdir'.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(c9xbj48h(dbzrmqz9bw4s5v(5$x5pu50#icd5&=2dimrp)r^#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if is_test_or_prod == True else True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
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
]

ROOT_URLCONF = 'shuaibb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'shuaibb.wsgi.application'


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'users.User'


ATOMIC_REQUESTS =True

REST_FRAMEWORK = {
    # authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    # renderer
    'DEFAULT_RENDERER_CLASSES': [
        'shuaibb.renderers.CustomJsonRenderer',
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # exception
    'EXCEPTION_HANDLER': 'shuaibb.exceptions.custom_exception_handler'
}

INSTALLED_APPS += [
    "rest_framework",
    'rest_framework.authtoken',
    "corsheaders",
    'shuaibb.app.ShuaibbConfig',
    'users',
    'samples',
    'upload',
    'pictures',
    'schedules',
    'customers',
    'auths'
]

MIDDLEWARE += [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': ENV_CONFIG.get('DB_NAME'), # database name
        'USER': ENV_CONFIG.get("DB_USER"),
        'PASSWORD': ENV_CONFIG.get("DB_PWD"),
        'HOST': ENV_CONFIG.get("DB_HOST"),
        'PORT': ENV_CONFIG.get("DB_PORT"),
    }
}


#### django-cors-headers start ####
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://101.42.247.31:9000"
]

CORS_ALLOWED_ORIGIN_REGEXES = [

]

CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_METHODS = (
    *default_methods,
)

CORS_ALLOW_HEADERS = (
    *default_headers,
)

CORS_ALLOW_CREDENTIALS = True
#### django-cors-headers end ####

############ upload ##############

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'


DEFAULT_FILE_STORAGE = "tencentcos_storage.TencentCOSStorage"
############ upload end ##############

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'users.backends.EmailAndMobileBackend',
)


