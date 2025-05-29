from azure.storage.blob import BlobServiceClient, ContentSettings
from django.conf import settings
import uuid
import os
import mimetypes

def upload_image_to_azure(file_input):
    # Build Azure blob service client
    account_url = f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url=account_url, credential=settings.AZURE_STORAGE_ACCOUNT_KEY)

    # Connect to the container
    container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER_NAME)

    # Determine filename
    if isinstance(file_input, str):  # it's a file path
        file_path = file_input
        file_name = os.path.basename(file_path)
        unique_filename = f"{uuid.uuid4()}_{file_name}"
        content_type, _ = mimetypes.guess_type(file_path)
        content_type = content_type or "application/octet-stream"
        with open(file_path, "rb") as file_data:
            blob_client = container_client.get_blob_client(unique_filename)
            blob_client.upload_blob(
                file_data,
                overwrite=True,
                content_settings=ContentSettings(
                    content_type=content_type,
                    content_disposition='inline'
                )
            )
    else:  # assume it's a file-like object
        file_name = file_input.name
        unique_filename = f"{uuid.uuid4()}_{file_name}"
        content_type, _ = mimetypes.guess_type(file_name)
        content_type = content_type or "application/octet-stream"
        blob_client = container_client.get_blob_client(unique_filename)
        blob_client.upload_blob(
            file_input,
            overwrite=True,
            content_settings=ContentSettings(
                content_type=content_type,
                content_disposition='inline'
            )
        )

    return f"{settings.AZURE_BLOB_URL}/{unique_filename}"


    # if isinstance(file_input, str):  # it's a file path
    #     file_path = file_input
    #     file_name = os.path.basename(file_path)
    #     unique_filename = f"{uuid.uuid4()}_{file_name}"
    #     with open(file_path, "rb") as file_data:
    #         blob_client = container_client.get_blob_client(unique_filename)
    #         blob_client.upload_blob(file_data, overwrite=True)
    # else:  # assume it's a file-like object
    #     unique_filename = f"{uuid.uuid4()}_{file_input.name}"
    #     blob_client = container_client.get_blob_client(unique_filename)
    #     blob_client.upload_blob(file_input, overwrite=True)


    # Create a unique filename to avoid collisions
    # unique_filename = f"{uuid.uuid4()}_{file_input.name}"
    # # Upload the blob
    # blob_client = container_client.get_blob_client(unique_filename)
    # blob_client.upload_blob(file_input, overwrite=True)

    # Return the public URL of the uploaded image
    return f"{settings.AZURE_BLOB_URL}/{unique_filename}"
