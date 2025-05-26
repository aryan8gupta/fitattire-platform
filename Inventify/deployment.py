import os 
import pymongo
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://inventory-management-app-hnbvgqaag3g2hyde.centralindia-01.azurewebsites.net/']
DEBUG = False
SECRET_KEY = 'django-insecure-$j$mcen!5kw_vxos#q9g)cm!@zflik7k3&nohn@rg_&qx!88hl'
PUBLIC_KEY = 'Aryan971pass'

ENVIRONMENT = "deployment"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    'https://inventory-management-app-hnbvgqaag3g2hyde.centralindia-01.azurewebsites.net/' 
]


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


ROOT_URLCONF = 'Inventify.urls'

WSGI_APPLICATION = 'Inventify.wsgi.application'

    
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

my_var = os.getenv('Azure_Cosmos_Conn', 'Default Value-1')

CONNECTION = pymongo.MongoClient(my_var, serverSelectionTimeoutMS=30000, retryWrites=True)
logger.info(CONNECTION)

DB = CONNECTION['inventory-management']

logger.info("1234")


# DB = {s
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'inventory-management-app-database',  # Name of your database
#         'CLIENT': {
#             'host': 'mongodb://inventory-management-app-server.mongo.cosmos.azure.com:10255/',  # Replace with your URI
#             'port': 10255,  # Default port for Azure Cosmos DB Mongo API
#             'username': 'inventory-management-app-server',  # Your account name
#             'password': os.getenv('Azure_Cosmos_Pswd'),  # Your primary key
#             'authSource': 'admin',
#             'authMechanism': 'SCRAM-SHA-256',
#             'tls': True,
#         },
#     }
# }


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'