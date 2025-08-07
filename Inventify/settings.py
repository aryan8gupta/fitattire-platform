import os
from .base import *

try:
    from .deployment import *
except ImportError:
    pass

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ENVIRONMENT = "local"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

Django_Key = os.getenv('DJANGO_SECRET_KEY', 'Default Value-4')
SECRET_KEY = Django_Key

JWT_Key = os.getenv('JWT_SECRET_KEY_VERIFICATION', 'Default Value-3')
JWT_SECRET_KEY = JWT_Key


CSRF_TRUSTED_ORIGINS = ['https://inventory-management-app-hnbvgqaag3g2hyde.centralindia-01.azurewebsites.net/']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

AZURE_KEY_VAULT_URL = os.environ.get('AZURE_KEY_VAULT_URL', 'https://inventify-kms-vault-8447.vault.azure.net/') # MAKE SURE THIS MATCHES YOUR KEY VAULT'S URL EXACTLY
AZURE_KEY_VAULT_KEY_NAME = os.environ.get('AZURE_KEY_VAULT_KEY_NAME', 'image-encryption-key') # MAKE SURE THIS MATCHES THE KEY NAME YOU JUST CREATED

Blob_Key = os.getenv('Blob_Account_Key', 'Default Value-1')

AZURE_STORAGE_ACCOUNT_NAME = "fitattirestorage"
AZURE_STORAGE_ACCOUNT_KEY = Blob_Key
AZURE_CONTAINER_NAME = "fitattire-assets"

AZURE_BLOB_URL = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER_NAME}"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Inventify'
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

ROOT_URLCONF = 'Inventify.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, "templates"],
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

WSGI_APPLICATION = 'Inventify.wsgi.application'
    
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# For Local
# import pymongo
# CONNECTION = pymongo.MongoClient('mongodb://localhost:27017')
# DB = CONNECTION.fitattire


# For Production
import pymongo
my_var = os.getenv('Azure_Cosmos_Conn', 'Default Value')

CONNECTION = pymongo.MongoClient(my_var, serverSelectionTimeoutMS=30000, retryWrites=False)
logger.info(CONNECTION)

DB = CONNECTION['inventory-management']



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata' 

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# For Locally
# STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     BASE_DIR / "static",
# ]


# For Production
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'