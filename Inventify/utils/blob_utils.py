from azure.storage.blob import BlobServiceClient
from django.conf import settings
import uuid

def upload_image_to_azure(file_obj):
    # Build Azure blob service client
    account_url = f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url=account_url, credential=settings.AZURE_STORAGE_ACCOUNT_KEY)

    # Connect to the container
    container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER_NAME)

    # Create a unique filename to avoid collisions
    unique_filename = f"{uuid.uuid4()}_{file_obj.name}"

    # Upload the blob
    blob_client = container_client.get_blob_client(unique_filename)
    blob_client.upload_blob(file_obj, overwrite=True)

    # Return the public URL of the uploaded image
    return f"{settings.AZURE_BLOB_URL}/{unique_filename}"
