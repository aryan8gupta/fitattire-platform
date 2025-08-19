from azure.storage.blob import BlobServiceClient, ContentSettings
from django.conf import settings
import uuid
import os
import mimetypes
import re
import io
from urllib.parse import urlparse
# from Inventify.utils.kms_utils import encrypt_with_kms, decrypt_with_kms
import logging
logger = logging.getLogger(__name__)
from Inventify.settings import DEBUG

# if DEBUG:
#     # In local development (DEBUG=True), use the mock KMS functions
#     from Inventify.utils.kms_mock_utils import encrypt_with_kms, decrypt_with_kms
#     logger.warning("--- Using MOCK KMS utilities for local development ---")
# else:
#     # In production/staging (DEBUG=False), use the real KMS functions
#     from Inventify.utils.kms_utils import encrypt_with_kms, decrypt_with_kms
#     logger.info("--- Using REAL KMS utilities for production/staging ---")



def download_and_decrypt_image_from_azure(encrypted_blob_url):
    """
    Downloads an encrypted blob from Azure Blob Storage, decrypts its content
    using KMS, and returns the plaintext image data as a BytesIO object.

    Args:
        encrypted_blob_url (str): The full URL of the encrypted blob in Azure.

    Returns:
        io.BytesIO: A BytesIO object containing the plaintext image data.
    """
    account_url = f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url=account_url, credential=settings.AZURE_STORAGE_ACCOUNT_KEY)

    # Extract container name and blob name from the URL
    parsed_url = urlparse(encrypted_blob_url)
    # The path usually starts with /container_name/blob_path
    path_segments = parsed_url.path.strip('/').split('/')
    if len(path_segments) < 2:
        logger.error(f"Invalid Azure blob URL format for decryption: {encrypted_blob_url}")
        raise ValueError(f"Invalid Azure blob URL format: {encrypted_blob_url}")
    
    container_name_from_url = path_segments[0]
    blob_name_from_url = '/'.join(path_segments[1:])

    container_client = blob_service_client.get_container_client(container_name_from_url)
    blob_client = container_client.get_blob_client(blob_name_from_url)

    try:
        # Download the encrypted blob content
        download_stream = blob_client.download_blob()
        encrypted_image_data = download_stream.readall()
        logger.debug(f"Encrypted image data downloaded from {encrypted_blob_url}")

        # --- KMS DECRYPTION OF THE IMAGE DATA ITSELF ---
        plaintext_image_data = decrypt_with_kms(encrypted_image_data)
        logger.debug(f"Image data decrypted for {encrypted_blob_url}")

        # Return as BytesIO object, which is suitable for PIL and other image processing libraries
        return io.BytesIO(plaintext_image_data)

    except Exception as e:
        logger.error(f"Failed to download and decrypt image from Azure Blob: {encrypted_blob_url}. Error: {e}", exc_info=True)
        raise # Re-raise the exception to indicate failure




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
    

    # Determine the final blob name in Azure
    filename = None

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


def upload_audio_to_azure(file_input):
    # Initialize blob service
    account_url = f"https://{settings.AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(account_url=account_url, credential=settings.AZURE_STORAGE_ACCOUNT_KEY)
    container_client = blob_service_client.get_container_client(settings.AZURE_CONTAINER_NAME)

    def get_next_azure_audio_filename(container_client, prefix, extension, subfolder):
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
    else:  # File-like object
        try:
            file_name = file_input.name
        except AttributeError:
            file_name = "default_audio.mp3"
        extension = file_name.split(".")[-1].lower()
        content_type, _ = mimetypes.guess_type(file_name)

    content_type = content_type or "audio/mpeg"  # default fallback

    # Generate final blob name
    prefix = "background_audio"
    subfolder = "audios"
    filename = get_next_azure_audio_filename(container_client, prefix, extension, subfolder)
    blob_name = f"output/{filename}"

    # Upload to Azure
    blob_client = container_client.get_blob_client(blob_name)

    if isinstance(file_input, str):
        with open(file_input, "rb") as audio_data:
            blob_client.upload_blob(
                audio_data,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type)
            )
    else:
        blob_client.upload_blob(
            file_input,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type)
        )

    # Return full Azure URL
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


# blob_path = f"output/upscaled/result_image-108.jpg"
# delete_file = delete_blob_from_azure(blob_path)

# for i in range(4, 108):
#     blob_path = f"output/upscaled/result_image-{i}.jpg"
#     delete_file = delete_blob_from_azure(blob_path)
