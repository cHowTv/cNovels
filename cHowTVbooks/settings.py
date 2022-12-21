"""
Django settings for cHowTVbooks project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from datetime import timedelta
from pathlib import Path
import os
from os import environ as env

from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = env['SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'novel',
    'user',
    'api',
    'author',
    'ckeditor',
    'star_ratings',
    'corsheaders',
     "dj_rest_auth",
    "allauth",
    'django_filters',
    "multiselectfield",
    "allauth.account",
    "django.contrib.sites",
    "dj_rest_auth.registration",
    "allauth.socialaccount",
    'drf_spectacular',
    'django_rest_passwordreset',
    'rest_framework_simplejwt.token_blacklist',
   "allauth.socialaccount.providers.google",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware' 
]

ROOT_URLCONF = 'cHowTVbooks.urls'

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

WSGI_APPLICATION = 'cHowTVbooks.wsgi.application'

AUTH_USER_MODEL = 'novel.User'
DEFAULT_AUTO_FIELD='django.db.models.AutoField'
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Allow all cors
CORS_ALLOW_ALL_ORIGINS = DEBUG

# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:3030',
#     'https://c-novels-frontend.vercel.app'
# ]

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT =  os.path.join(BASE_DIR, 'novel/static')

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
       #  'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.IsAuthenticated'
    ],
    'EXCEPTION_HANDLER': 'api.utils.custom_response.custom_exception_handler',

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

 
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_CONFIGS = {
    'default':
    {
        'toolbar':'Custom',
        'height': 500,
       
        
        'toolbar_Custom': [
            ['Unlink', 'Link' , 'Image'],
            ['Styles', 'Format', 'Bold', 'Italic', 'SpellChecker', 'Undo', 'Redo'],
            ['Smiley', 'SpecialChar'],
            ['CodeSnippet', 'about']
        ],
        'extraPlugins':'codesnippet'
    },
    'novellas':{
        'toolbar':'Custom',
        'height': 500,
        'width': '105%',
        'display': 'inline-block',
        'placeholder': 'maximize to start writing',
        
        'toolbar_Custom': [
          
            ['Styles', 'Format', 'Bold', 'Italic', 'SpellChecker', 'Undo', 'Redo'],
            ['Smiley', 'SpecialChar'],
            ['Indent', 'Outdent','Maximize'],
            ['JustifyLeft', 'JustifyCenter','JustifyRight','JustifyBlock']
        ],
        
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'



SIMPLE_JWT = {
        
        'REFRESH_TOKEN_LIFETIME':   timedelta(days=15),
        'ROTATE_REFRESH_TOKENS': True,
        'BLACKLIST_AFTER_ROTATION': True, 
        'UPDATE_LAST_LOGIN': True,
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
REST_USE_JWT = True
SITE_ID = 1
LOGIN_REDIRECT_URL = '/login'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SWAGGER_SETTINGS = {'DEFAULT_AUTO_SCHEMA_CLASS': 'novel.views.CustomAutoSchema', 'TAGS_SORTER': 'none'}


REDOC_SETTINGS = {
   'LAZY_RENDERING': False,
   
}


EMAIL_BACKEND = env['EMAIL_BACKEND']
EMAIL_HOST = env['EMAIL_HOST']
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = env['EMAIL_HOST_PASSWORD']


