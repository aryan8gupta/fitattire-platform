import os 
import pymongo
from .base import *
from .base import BASE_DIR

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://inventory-management-app-hnbvgqaag3g2hyde.centralindia-01.azurewebsites.net/']
DEBUG = False
SECRET_KEY = 'django-insecure-$j$mcen!5kw_vxos#q9g)cm!@zflik7k3&nohn@rg_&qx!88hl'
PUBLIC_KEY = 'Aryan971pass'

ENVIRONMENT = "deployment"

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

    
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure Blob Connection
Blob_Key = os.getenv('Blob_Account_Key', 'Default Value-1')

AZURE_STORAGE_ACCOUNT_NAME = "fitattirestorage"
AZURE_STORAGE_ACCOUNT_KEY = Blob_Key
AZURE_CONTAINER_NAME = "fitattire-assets"

AZURE_BLOB_URL = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net/{AZURE_CONTAINER_NAME}"

# Azure Database Connection
my_var = os.getenv('Azure_Cosmos_Conn', 'Default Value-1')

CONNECTION = pymongo.MongoClient(my_var, serverSelectionTimeoutMS=30000, retryWrites=False)
logger.info(CONNECTION)

DB = CONNECTION['inventory-management']


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
