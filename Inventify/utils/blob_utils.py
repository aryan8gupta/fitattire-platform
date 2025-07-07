from azure.storage.blob import BlobServiceClient, ContentSettings
from django.conf import settings
import uuid
import os
import mimetypes
import re
from urllib.parse import urlparse


def upload_image_to_azure(file_input, blob_name=None):
    # Build Azure blob service client
    account_url = f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url=account_url, credential=settings.AZURE_STORAGE_ACCOUNT_KEY)

    # Connect to the container
    container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER_NAME)

    def get_next_azure_filename(container_client, prefix, extension, subfolder):
        # List all blobs in the specified folder
        folder = f"output/{subfolder}" 
        blobs_list = container_client.list_blobs(name_starts_with=folder + "/")

        pattern = re.compile(rf"{re.escape(prefix)}-(\d+)\.{re.escape(extension)}")
        numbers = []

        for blob in blobs_list:
            blob_name = os.path.basename(blob.name)  # Extract just the filename
            match = pattern.match(blob_name)
            if match:
                numbers.append(int(match.group(1)))

        next_number = max(numbers) + 1 if numbers else 1
        return f"{subfolder}/{prefix}-{next_number}.{extension}"
    
    if (blob_name == "result"):
        filename = get_next_azure_filename(container_client, 'result_image', 'jpg', 'upscaled')
    elif (blob_name == "garment"):
        filename = get_next_azure_filename(container_client, 'garment_image', 'jpg', 'garment')
    elif (blob_name == "generated"):
        filename = get_next_azure_filename(container_client, 'generated_text_image', 'jpg', 'generated')
    elif (blob_name == "shop_logo"):
        filename = get_next_azure_filename(container_client, 'shop_logo', 'jpg', 'shop_logo')
    elif (blob_name == "tempfiles"):
        filename = get_next_azure_filename(container_client, 'tempfiles', 'jpg', 'tempfiles')

    blob_name = f"output/{filename}"


    # Determine filename
    if isinstance(file_input, str):  # File path
        file_path = file_input
        file_name = os.path.basename(file_path)
        content_type, _ = mimetypes.guess_type(file_path)
        content_type = content_type or "application/octet-stream"
        
        # Set blob name
        final_blob_name = blob_name or f"{uuid.uuid4()}_{file_name}"

        # Upload from file
        with open(file_path, "rb") as file_data:
            blob_client = container_client.get_blob_client(final_blob_name)
            blob_client.upload_blob(
                file_data,
                overwrite=True,
                content_settings=ContentSettings(
                    content_type=content_type,
                    content_disposition="inline"
                )
            )

    else:  # Assume file-like object (e.g., BytesIO)
        try:
            file_name = file_input.name
        except AttributeError:
            file_name = "generated_image.png"  # fallback

        content_type, _ = mimetypes.guess_type(file_name)
        content_type = content_type or "application/octet-stream"

        final_blob_name = blob_name or f"{uuid.uuid4()}_{file_name}"

        blob_client = container_client.get_blob_client(final_blob_name)
        blob_client.upload_blob(
            file_input,
            overwrite=True,
            content_settings=ContentSettings(
                content_type=content_type,
                content_disposition="inline"
            )
        )

    # Return full blob URL
    return f"{settings.AZURE_BLOB_URL}/{final_blob_name}"


def upload_video_to_azure(file_input):
    # Initialize blob service
    account_url = f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url=account_url, credential=settings.AZURE_STORAGE_ACCOUNT_KEY)
    container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER_NAME)

    def get_next_azure_video_filename(container_client, prefix, extension, subfolder):
        folder = f"output/{subfolder}"
        blobs_list = container_client.list_blobs(name_starts_with=folder + "/")

        pattern = re.compile(rf"{re.escape(prefix)}-(\d+)\.{re.escape(extension)}")
        numbers = []

        for blob in blobs_list:
            blob_name = os.path.basename(blob.name)
            match = pattern.match(blob_name)
            if match:
                numbers.append(int(match.group(1)))

        next_number = max(numbers) + 1 if numbers else 1
        return f"{subfolder}/{prefix}-{next_number}.{extension}"

    # Determine filename, extension, and content type
    if isinstance(file_input, str):  # File path
        file_path = file_input
        file_name = os.path.basename(file_path)
        extension = file_name.split(".")[-1].lower()
        content_type, _ = mimetypes.guess_type(file_path)
    else:  # File-like object (BytesIO or InMemoryUploadedFile)
        try:
            file_name = file_input.name
        except AttributeError:
            file_name = "default_video.mp4"
        extension = file_name.split(".")[-1].lower()
        content_type, _ = mimetypes.guess_type(file_name)

    content_type = content_type or "video/mp4"  # default fallback

    # Generate final blob name
    prefix = "variant_video"
    subfolder = "videos"
    filename = get_next_azure_video_filename(container_client, prefix, extension, subfolder)
    blob_name = f"output/{filename}"

    # Upload
    blob_client = container_client.get_blob_client(blob_name)

    if isinstance(file_input, str):
        with open(file_input, "rb") as video_data:
            blob_client.upload_blob(
                video_data,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type)
            )
    else:
        blob_client.upload_blob(
            file_input,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type)
        )

    # Return Azure Blob URL
    return f"{settings.AZURE_BLOB_URL}/{blob_name}"


def extract_blob_path_from_url(url):
    """
    Converts full URL to just the blob path.
    Example:
    https://your.blob.core.windows.net/container/output/tempfiles/img-1.jpg
    ➜ output/tempfiles/img-1.jpg
    """
    path = urlparse(url).path  # /container/output/tempfiles/xyz.jpg
    parts = path.strip("/").split("/", 1)  # remove leading slash, split once
    return parts[1] if len(parts) > 1 else None


def delete_blob_from_azure(blob_path):
    """
    Deletes a blob like: output/upscaled/result_image-23.jpg
    """
    account_url = f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url=account_url, credential=settings.AZURE_STORAGE_ACCOUNT_KEY)
    container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER_NAME)

    try:
        blob_client = container_client.get_blob_client(blob_path)
        blob_client.delete_blob()
        print(f"🗑️ Deleted blob: {blob_path}")
    except Exception as e:
        print(f"❌ Failed to delete blob: {blob_path} | Error: {e}")