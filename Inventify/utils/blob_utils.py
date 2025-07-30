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

    # if blob_name == "result":
    #     generated_filename = get_next_azure_filename(container_client, 'result_image', 'jpg', 'upscaled')
    # elif blob_name == "garment":
    #     generated_filename = get_next_azure_filename(container_client, 'garment_image', 'jpg', 'garment')
    # elif blob_name == "generated":
    #     generated_filename = get_next_azure_filename(container_client, 'generated_text_image', 'jpg', 'generated')
    # elif blob_name == "shop_logo":
    #     generated_filename = get_next_azure_filename(container_client, 'shop_logo', 'jpg', 'shop_logo')
    # elif blob_name == "tempfiles":
    #     generated_filename = get_next_azure_filename(container_client, 'tempfiles', 'jpg', 'tempfiles')

    # # Fallback if no specific prefix matched, or if blob_name_prefix is None
    # final_blob_name = f"output/{generated_filename}" if generated_filename else \
    #                   f"output/{uuid.uuid4()}_{file_input.name if hasattr(file_input, 'name') else 'unknown_file.jpg'}"

    # image_data_bytes = None
    # original_content_type = None

    # # Read the image data into bytes
    # if isinstance(file_input, str):  # File path
    #     file_path = file_input
    #     original_content_type, _ = mimetypes.guess_type(file_path)
    #     original_content_type = original_content_type or "application/octet-stream"
    #     with open(file_path, "rb") as file_data:
    #         image_data_bytes = file_data.read()
    # elif hasattr(file_input, 'read') and callable(file_input.read):  # File-like object (Django UploadedFile, BytesIO)
    #     # Ensure the file_input's cursor is at the beginning if it was read previously
    #     file_input.seek(0)
    #     image_data_bytes = file_input.read()
    #     try: # Try to get content type (e.g., from Django's UploadedFile)
    #         original_content_type = file_input.content_type
    #     except AttributeError: # Fallback for generic file-like objects
    #         file_name = file_input.name if hasattr(file_input, 'name') else "generated_image.png"
    #         original_content_type, _ = mimetypes.guess_type(file_name)
    #         original_content_type = original_content_type or "application/octet-stream"
    # else:
    #     logger.error(f"Unsupported file_input type for upload_image_to_azure: {type(file_input)}")
    #     raise ValueError("Unsupported file_input type provided to upload_image_to_azure")

    # if not image_data_bytes:
    #     raise ValueError("No image data extracted for upload.")

    # # --- KMS ENCRYPTION OF THE IMAGE DATA ITSELF ---
    # encrypted_image_data = encrypt_with_kms(image_data_bytes)
    # logger.debug(f"Image data encrypted for blob: {final_blob_name}")

    # # Upload the ENCRYPTED data to Azure
    # blob_client = container_client.get_blob_client(final_blob_name)
    # blob_client.upload_blob(
    #     encrypted_image_data, # Upload the encrypted bytes
    #     overwrite=True,
    #     content_settings=ContentSettings(
    #         # For encrypted blobs, the content type should typically be generic binary
    #         content_type="application/octet-stream",
    #         content_disposition="inline" # Still inline if you want it to be viewable (after decryption)
    #     )
    # )
    # logger.info(f"Encrypted image uploaded to Azure: {final_blob_name}")

    # # Return full blob URL of the ENCRYPTED blob
    # return f"{settings.AZURE_BLOB_URL}/{final_blob_name}"



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