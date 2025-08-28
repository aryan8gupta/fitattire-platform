import requests
import os
import time
import uuid
from PIL import Image, ImageOps
from urllib.request import urlopen
from io import BytesIO
from Inventify.utils.blob_utils import upload_image_to_azure, delete_blob_from_azure, extract_blob_path_from_url

my_var1 = os.getenv('Instagram_Access_Token', 'Default Value')
my_var2 = os.getenv('Instagram_Business_Account_ID', 'Default Value')

ACCESS_TOKEN = my_var1
INSTAGRAM_BUSINESS_ACCOUNT_ID = my_var2


def post_carousel_to_instagram(image_list, caption):

    def resize_url_image_to_4_5(image_url):
        try:
            # Step 1: Download image
            response = urlopen(image_url)
            img = Image.open(BytesIO(response.read()))

            img.info.clear()

            # Step 2: Convert if needed
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Step 3: Resize or pad to 4:5 aspect ratio
            W, H = img.size
            target_ratio = 4 / 5
            current_ratio = W / H

            if current_ratio > target_ratio:
                # Image too wide — pad top/bottom
                new_height = int(W / target_ratio)
                pad = (new_height - H) // 2
                img = ImageOps.expand(img, (0, pad), fill="white")
            elif current_ratio < target_ratio:
                # Image too tall — pad left/right
                new_width = int(H * target_ratio)
                pad = (new_width - W) // 2
                img = ImageOps.expand(img, (pad, 0), fill="white")
            # else: already 4:5 — do nothing


            # Step 4: Save to BytesIO instead of local file
            buffer = BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)  # Reset pointer

            # Step 5: Upload to Azure directly
            buffer.name = "resized_image.jpg"  # Required for mimetype detection
            azure_url = upload_image_to_azure(buffer, "tempfiles")

            # 💥 Add a cache-busting query
            image_url = f"{azure_url}?nocache={uuid.uuid4()}"

            return image_url

        except Exception as e:
            print(f"❌ Error: {e}")


    def post_carousel_to_instagram(azure_image_urls, caption):
        uploaded_media_ids = []
        print("🚀 Number of image URLs:", len(azure_image_urls))

        # ✅ Upload each image as carousel item
        for idx, image_url in enumerate(azure_image_urls):
            print(f"Uploading image {idx + 1}/{len(azure_image_urls)}")
            media_payload = {
                'image_url': image_url,
                'is_carousel_item': True,   # ✅ USE BOOLEAN
                'media_type': 'IMAGE', 
                'access_token': ACCESS_TOKEN
            }
            media_url = f"https://graph.facebook.com/v22.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
            response = requests.post(media_url, data=media_payload)
            result = response.json()
            print("Upload Response:", result)

            if response.status_code == 200 and 'id' in result:
                uploaded_media_ids.append(result['id'])
            else:
                print("❌ Failed to upload image:", result)
                return {"status": "error", "details": result}

            time.sleep(1)  # avoid rate limits

        print("✅ Uploaded Media IDs:", uploaded_media_ids)
        print("Count:", len(uploaded_media_ids))

        if len(uploaded_media_ids) < 2:
            print("❌ Cannot post carousel with less than 2 images.")
            return {"status": "error", "reason": "Too few images"}

        children_array = ','.join(uploaded_media_ids)
        time.sleep(5)

        # ✅ Create carousel container
        print("Creating carousel...")
        carousel_payload = {
            'children': children_array,  # ✅ Must be comma-separated string, not a list
            'caption': caption,
            'media_type': 'CAROUSEL',
            'access_token': ACCESS_TOKEN
        }


        carousel_response = requests.post(
            f"https://graph.facebook.com/v22.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media",
            data=carousel_payload  # ✅ Send as form data, not JSON
        )


        carousel_result = carousel_response.json()
        print("Carousel Create Response:", carousel_result)

        if 'id' not in carousel_result:
            return {"status": "error", "details": carousel_result}

        creation_id = carousel_result['id']

        # ✅ Publish the carousel post
        # publish_url = f"https://graph.facebook.com/v22.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
        # publish_payload = {
        #     'creation_id': creation_id,
        #     'access_token': ACCESS_TOKEN
        # }
        # publish_response = requests.post(publish_url, data=publish_payload)
        # publish_result = publish_response.json()
        # print("✅ Publish Response:", publish_result)

        # return {
        #     "status": "success",
        #     "carousel_creation_id": creation_id,
        #     "publish_response": publish_result
        # }

    resized_image_urls = []
    for i, url in enumerate(image_list):
        result = ''
        result = resize_url_image_to_4_5(url)
        if result:
            resized_image_urls.append(result)

    print("✅ Resized images:", resized_image_urls)

    post_carousel_to_instagram(resized_image_urls, caption)

    for image_url in resized_image_urls:
        blob_path = extract_blob_path_from_url(image_url)
        if blob_path:
            delete_blob_from_azure(blob_path)



def post_to_instagram(image_url, caption):
    # Step 1: Create media object
    create_url = f'https://graph.facebook.com/v22.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media'
    print("1/2")
    create_payload = {
        'image_url': image_url,
        'caption': caption,
        'access_token': ACCESS_TOKEN,
    }
    create_resp = requests.post(create_url, data=create_payload)
    print("Media Creation Response:", create_resp.json())

    if create_resp.status_code == 200:
        creation_id = create_resp.json().get('id')
        print("Creation ID:", creation_id)

        # Step 2: Publish the media
        publish_url = f'https://graph.facebook.com/v22.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish'
        publish_payload = {
            'creation_id': creation_id,
            'access_token': ACCESS_TOKEN,
        }
        publish_resp = requests.post(publish_url, data=publish_payload)
        print("Publish Response:", publish_resp.json())

        return {
            "status": "success",
            "creation_id": creation_id,
            "publish_response": publish_resp.json()
        }

    else:
        print("Failed to create media object")
        return {
            "status": "error",
            "error": create_resp.json()
        }


def post_azure_video_to_instagram(video_url, caption):
    # Step 1: Create media object with video
    create_url = f'https://graph.facebook.com/v22.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media'
    create_payload = {
        'media_type': 'REELS',
        'video_url': video_url,
        'caption': caption,
        'access_token': ACCESS_TOKEN,
    }
    create_resp = requests.post(create_url, data=create_payload)
    print("Media Creation Response:", create_resp.json())

    if create_resp.status_code != 200:
        return {
            "status": "error",
            "step": "media_creation",
            "error": create_resp.json()
        }

    creation_id = create_resp.json().get('id')
    print("Creation ID:", creation_id)

    # Step 2: Poll for video processing status
    while True:
        status_url = f'https://graph.facebook.com/v22.0/{creation_id}?fields=status_code&access_token={ACCESS_TOKEN}'
        status_resp = requests.get(status_url)
        status = status_resp.json().get("status_code")
        print("Processing Status:", status)

        if status == "FINISHED":
            break
        elif status == "ERROR":
            return {
                "status": "error",
                "step": "processing",
                "error": status_resp.json()
            }

        time.sleep(3)

    # Step 3: Publish to Instagram
    publish_url = f'https://graph.facebook.com/v22.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish'
    publish_payload = {
        'creation_id': creation_id,
        'access_token': ACCESS_TOKEN,
    }
    publish_resp = requests.post(publish_url, data=publish_payload)
    print("Publish Response:", publish_resp.json())

    if publish_resp.status_code == 200:
        return {
            "status": "success",
            "creation_id": creation_id,
            "publish_response": publish_resp.json()
        }
    else:
        return {
            "status": "error",
            "step": "publishing",
            "error": publish_resp.json()
        }
