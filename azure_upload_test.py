from azure.storage.blob import BlobServiceClient, ContentSettings
from django.conf import settings
import mimetypes
from Inventify.settings import AZURE_STORAGE_ACCOUNT_NAME, AZURE_STORAGE_ACCOUNT_KEY, AZURE_CONTAINER_NAME, AZURE_BLOB_URL, BASE_DIR


def upload_image_to_azure(file_input, blob_name):

    account_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
    blob_service_client = BlobServiceClient(
        account_url=account_url,
        credential=AZURE_STORAGE_ACCOUNT_KEY
    )
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

    # --- Read image bytes ---
    if isinstance(file_input, str):  # File path
        content_type, _ = mimetypes.guess_type(file_input)
        content_type = content_type or "application/octet-stream"
        with open(file_input, "rb") as f:
            image_data = f.read()
    elif hasattr(file_input, "read"):  # File-like
        file_input.seek(0)
        image_data = file_input.read()
        file_name = getattr(file_input, 'name', 'image.png')
        content_type, _ = mimetypes.guess_type(file_name)
        content_type = content_type or "application/octet-stream"
    else:
        raise ValueError(f"Unsupported file_input type: {type(file_input)}")

    # --- Upload to Azure ---
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(
        image_data,
        overwrite=True,
        content_settings=ContentSettings(content_type=content_type, content_disposition="inline")
    )

    return f"{AZURE_BLOB_URL}/{blob_name}"


import os

local_path = os.path.join(BASE_DIR, "static/img/models/men/shirts/full-sleeve-shirts/casual-shirts/casual-shirts-1.png")

# Confirm it exists now
print("Resolved Path:", local_path)
print("Exists:", os.path.exists(local_path))


azure_url1 = upload_image_to_azure(
    "static/img/models/men/shirts/full-sleeve-shirts/casual-shirts/casual-shirts-1.png",
    "men:shirts:full-sleeve-shirts:casual-shirts:casual-shirts-1.png"
)
azure_url3 = upload_image_to_azure(
    "static/img/models/men/shirts/full-sleeve-shirts/casual-shirts/casual-shirts-2.png",
    "men:shirts:full-sleeve-shirts:casual-shirts:casual-shirts-2.png"
)
azure_url4 = upload_image_to_azure(
    "static/img/models/men/shirts/full-sleeve-shirts/formal-shirts/formal-shirts-1.png",
    "men:shirts:full-sleeve-shirts:formal-shirts:formal-shirts-1.png"
)

print("Uploaded to:", azure_url4)

