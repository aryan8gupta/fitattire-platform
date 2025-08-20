from django.conf import settings
from bson.son import SON
from django.contrib import messages;
from django.shortcuts import render, redirect;
from django.http import HttpResponseRedirect, HttpResponse

from collections import Counter
from collections import OrderedDict as SON
import bcrypt 
import jwt
from bson.objectid import ObjectId

from django.utils import timezone
from django.utils.timezone import localtime, make_aware, now
from datetime import timedelta, datetime, timezone as dt_timezone

from django.views.decorators.csrf import csrf_exempt

# from Inventify.settings import DB, JWT_SECRET_KEY, MEDIA_ROOT, DEBUG
from Inventify.deployment import DB, JWT_SECRET_KEY, MEDIA_ROOT

from .models import YourModel
from video_generator.generate_text_photos import create_dynamic_photo_with_auto_closeup_1, create_dynamic_photo_with_auto_closeup_2, create_offer_photo_with_right_image, create_offer_photo_with_right_image_2
from video_generator.instagram_post_test import post_to_instagram, post_azure_video_to_instagram, post_carousel_to_instagram
from video_generator.generate_video import start_video_generation, start_video_generation_2
from video_generator.send_whatsapp import send_invoice_whatsapp_message
from video_generator.collage_image import create_collage

# from Inventify.utils.encryption import derive_aes_key, decrypt_field_if_needed
# from Inventify.utils.kms_utils import encrypt_with_kms, decrypt_with_kms

from PIL import Image, ImageOps
from io import BytesIO
import zipfile
import threading
import uuid
import os
import re
import requests
import base64
import json
import time
import random
import string
from django.http import JsonResponse
from Inventify.utils.blob_utils import upload_image_to_azure, upload_audio_to_azure, download_and_decrypt_image_from_azure

from openai import OpenAI
import secrets

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# import tempfile
# if DEBUG:
#     # In local development (DEBUG=True), use the mock KMS functions
#     from Inventify.utils.kms_mock_utils import encrypt_with_kms, decrypt_with_kms
#     logger.warning("--- Using MOCK KMS utilities for local development ---")
# else:
#     # In production/staging (DEBUG=False), use the real KMS functions
#     from Inventify.utils.kms_utils import encrypt_with_kms, decrypt_with_kms
#     logger.info("--- Using REAL KMS utilities for production/staging ---")

my_var_2 = os.getenv('Open_API_Key', 'Default Value')
client = OpenAI(api_key=my_var_2)


PINCEL_API_URL = "https://pincel.app/api/clothes-swap"
my_var_1 = os.getenv('New_Pincel_API_Key', 'Default Value')
PINCEL_API_KEY = my_var_1


PICSART_API_KEY = "eyJraWQiOiI5NzIxYmUzNi1iMjcwLTQ5ZDUtOTc1Ni05ZDU5N2M4NmIwNTEiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJhdXRoLXNlcnZpY2UtYjU2NGRmNmUtZDA3OC00NjEzLTk1MWEtZmE0ZjZjM2JkNDA4IiwiYXVkIjoiNDkxNzQzNTgxMDAxMTAxIiwibmJmIjoxNzU0MDQ3NjIwLCJzY29wZSI6WyJiMmItYXBpLmdlbl9haSIsImIyYi1hcGkuaW1hZ2VfYXBpIl0sImlzcyI6Imh0dHBzOi8vYXBpLnBpY3NhcnQuY29tL3Rva2VuLXNlcnZpY2UiLCJvd25lcklkIjoiNDkxNzQzNTgxMDAxMTAxIiwiaWF0IjoxNzU0MDQ3NjE5LCJqdGkiOiIwNjQ5NGM5ZC0xZmU3LTQ1YjMtYmJiZS1iMmEwZjM2MzgyM2QifQ.JBrobUONLeYkOntj8V_g8_RVKcJUYoJWhTDc1wJO4QEiEHqC1N3fTgBDwJsohjtm2Yxh-OdgFv8YHBc5Lysr4_-kru1v_ZwNOx4sbs_0b5Y4MGqcB9M4cgySLoBoosJ00e7i7Dsc7cQcCKOx_qUMDhtK8Jlg6XHAhz4jJPLfFq6dlcJTv7lP3fN3MI3iiw8RB29gy8K2CKkiweMXavG-i5PhU23fz1MQ-X_1AF_HgEUItUmQEa9UWVedsiclP6oHGsNEAXrriqcz2m3adYeJBroVnAkzRCG1QdUyzxDlvMxPaDKNLKbIpDBwodCsEWoycMKlSXmvvEH6J44ksTN1oQ"


# QR-Code Generating / Template----------------------------------------------------------->
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

# === Label and Page Dimensions ===
LABEL_WIDTH_MM = 64
LABEL_HEIGHT_MM = 34
PAGE_WIDTH_MM = 210
PAGE_HEIGHT_MM = 297
TOP_MARGIN_MM = 1
LEFT_MARGIN_MM = 6
GAP_X_MM = 5   # Horizontal gap
GAP_Y_MM = 3   # ✅ MINIMAL vertical gap to fit 8 rows

def mm_to_pt(mm_val):
    return mm_val * mm

def generate_qr_code(data, filename):
    qr = qrcode.make(data)
    qr.save(filename)
    return filename

def create_qr_label_pdf(start_id=10000, total_labels=240, output_file="qr_labels-4.pdf"):
    c = canvas.Canvas(output_file, pagesize=(mm_to_pt(PAGE_WIDTH_MM), mm_to_pt(PAGE_HEIGHT_MM)))

    labels_per_row = 3
    labels_per_col = 8
    labels_per_page = labels_per_row * labels_per_col

    label_width = mm_to_pt(LABEL_WIDTH_MM)
    label_height = mm_to_pt(LABEL_HEIGHT_MM)
    gap_x = mm_to_pt(GAP_X_MM)
    gap_y = mm_to_pt(GAP_Y_MM)
    x_start = mm_to_pt(LEFT_MARGIN_MM)
    
    # ✅ Start from very top to fit full 8 rows
    y_start = mm_to_pt(PAGE_HEIGHT_MM - TOP_MARGIN_MM)

    text_width = label_width * 0.3
    qr_width = label_width * 0.7 - mm_to_pt(2)  # Leave 2mm gap between text and QR
    qr_height = label_height * 0.9


    for i in range(total_labels):
        qr_id = f"FIA-{start_id + i}"
        qr_data = f"https://fitattire.shop/product-display/{qr_id}/"
        qr_filename = f"qr_{qr_id}.png"

        generate_qr_code(qr_data, qr_filename)

        page_index = i // labels_per_page
        index_on_page = i % labels_per_page
        row = index_on_page // labels_per_row
        col = index_on_page % labels_per_row

        x = x_start + col * (label_width + gap_x)
        y = y_start - row * (label_height + gap_y) - label_height  # correct Y for each row

        # Draw text (left 30%)
        c.setFont("Helvetica", 8)
        c.drawRightString(x + text_width - mm_to_pt(1), y + label_height / 2, f"ID: {qr_id}")

        # Draw QR code (right 70%)
        qr_x = x + text_width + mm_to_pt(2)  # small gap after text
        c.drawImage(qr_filename, qr_x, y, width=qr_width, height=qr_height)

        if os.path.exists(qr_filename):
            os.remove(qr_filename)

        if (i + 1) % labels_per_page == 0:
            c.showPage()

    c.save()
    print(f"✅ PDF saved: {output_file}")
    print(f"📄 Full path: {os.path.abspath(output_file)}")



# create_qr_label_pdf(start_id=10001, total_labels=48)

# --------------------------------------------------------------------->

product_list1 = []

def generate_password(a):
    bytes = a.encode('utf-8') 
  
    # generating the salt 
    salt = bcrypt.gensalt() 
    
    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt) 
    return hash


def generate_token(user_dict):
    token = jwt.encode({"exp": localtime(timezone.now()) + timedelta(days=7) , **user_dict}, JWT_SECRET_KEY, algorithm="HS256")
    return token


def verify_token(token):
    
    decoded_token = {}  
    if token:
        try:
            decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms="HS256", options={"verify_exp": False})
        except Exception as e:
            return False, {}
    else:
        return False, {}
    
    return True, decoded_token

def health_check(request):
    return JsonResponse({"status": "ok"})

def index(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    # text = ["Price: ₹550", "Sizes: ['S'], ['M'], ['L']", "Fabric: Cotton", "Color: Red"]

    # image_url_1 = create_dynamic_photo_with_auto_closeup(
    #     big_image_path="https://fitattirestorage.blob.core.windows.net/fitattire-assets/c5e80186-20e0-41d0-b59a-edbb4464f4ad_final_upscaled-9.jpg",
    #     logo_path="https://fitattirestorage.blob.core.windows.net/fitattire-assets/Screenshot 2025-06-08 at 7.30.15 PM.png",
    #     texts=text,
    #     output_path="generated",
    #     garment_image_path="https://fitattirestorage.blob.core.windows.net/fitattire-assets/Screenshot 2025-03-15 at 9.56.31 AM.png"
    # )

    # image_url_2 = create_offer_photo_with_right_image(
    #     big_image_path="https://fitattirestorage.blob.core.windows.net/fitattire-assets/c5e80186-20e0-41d0-b59a-edbb4464f4ad_final_upscaled-9.jpg",
    #     output_path="generated",
    #     product_id="FIA-75913",
    #     offer_title="Mega Deal",
    #     discount_text="23% OFF",
    #     final_line_1="Mention the Product Id to",
    #     final_line_2="Know more."
    # )
    # image_url = image_url_1
    # caption = 'New Mega Deal Offer'

    # response = post_to_instagram(image_url, caption)

    # user_email = 'akshat@gmail.com'
    # user_record = DB.users.find_one({"email": user_email})
    # users_shop_address = user_record['shop_address']

    # generated_urls = ['https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/generated/generated_text_image-15.jpg', 'https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/generated/generated_text_image-34.jpg', 'https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/generated/generated_text_image-8.jpg']
    # video_output_path = "output/generated_reel_58.mp4"
    # video_url = start_video_generation(generated_urls, video_output_path, users_shop_address)
    print("2")


    return render(request, 'home.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})


def products_2(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    return render(request, 'products-2.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})


def product_display(request, qr_id):
    try: 
        valid = False
        data = {}
        if request.COOKIES.get('t'):
            valid, data = verify_token(request.COOKIES['t'])
        dashboard = None
        if valid:
            dashboard = 'dashboard'
        
        user_type = data.get('user_type')
        user_name = data.get('first_name')

        qrcode = qr_id + "/"

        result = DB.products.find_one({"qrcode_ids": qrcode})
        random_integer = random.randint(0, 50)
        if result:
            piece = "available"
            return render(request, 'product_display.html', {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, 'sold_count': random_integer, 'product': result, "show_edit": valid, 'product_id': qr_id, "piece": piece})
        else:
            result2 = DB.products_sold.find_one({
                "products": {
                    "$elemMatch": {
                        "qrcode_id": qrcode
                    }
                }
            })
            piece = "sold"
            if result2:
                return render(request, 'product_display.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, 'sold_count': random_integer, 'product': result2, "show_edit": valid, 'product_id': qr_id, "piece": piece})

        return render(request, 'product_display.html', {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, 'product': None})

    except Exception as e:
        print(f"Error in product_display: {e}")
        return render(request, 'product_display.html')



def invoice(request, invoice_id):

    records = list(DB.products_sold.find({"invoice_id": invoice_id}))
    if records:

        # Convert string fields like 'less' to float
        for r in records:
            try:
                r["less"] = float(r.get("less", 0))
            except (ValueError, TypeError):
                r["less"] = 0.0  # fallback if conversion fails

        user_id = records[0].get("user_id")
        users_shop_logo = ''
        users_shop_address = ''
        users_shop_name = ''
        users_phone = ''

        if user_id:
            user_record = DB.users.find_one({"_id": user_id})
            if user_record:
                users_shop_logo = user_record.get('shop_logo', '')
                users_shop_address = user_record.get('shop_address', '')
                users_shop_name = user_record.get('shop_name', '')
                users_phone = user_record.get('mobile', '')

    else:
        print("No Product Found")
        return render(request, 'invoice.html')

    return render(request, 'invoice.html',  {
        'records': records, 
        'products': [product for r in records for product in r.get('products', [])],
        'business_shop_logo': users_shop_logo,
        'business_shop_address': users_shop_address,
        'business_shop_name': users_shop_name,
        'business_phone': users_phone,
    })


def subscription(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    return render(request, 'subscription.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})

def subs_upgrade(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    return render(request, 'subs_upgrade.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})



def app_settings(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    return render(request, 'app_settings.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})


def scan_qr(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    return render(request, 'scan.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})


@csrf_exempt
def decrease_credits(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'

    user_email = data.get('email')

    if request.method == "POST":
        result = DB.users.find_one_and_update(
            {"email": user_email},
            {"$inc": {"credits_used": -1}},
            return_document=True
        )

        if result:
            return JsonResponse({"success": True, "new_credits": result['credits_used']})
        else:
            return JsonResponse({"success": False, "message": "Insufficient credits or user not found"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def get_garment_image(request):

    if request.method == 'POST':

        garment_image = request.FILES.get('garment_image')
        if not garment_image:
            return JsonResponse({'error': 'No image uploaded'}, status=400)

        from rembg import remove
        from PIL import Image, ImageChops

        # === Step 1: Remove Background ===
        def remove_background(input_path, output_path):
            input_image = Image.open(input_path).convert("RGBA")
            output_image = remove(input_image)
            output_image.save(output_path)
            return output_path

        # === Step 2: Auto-crop Transparent Area ===
        def autocrop_image(image_path, output_path):
            image = Image.open(image_path).convert("RGBA")
            bg = Image.new(image.mode, image.size, (0, 0, 0, 0))  # Transparent background
            diff = ImageChops.difference(image, bg)
            bbox = diff.getbbox()
            if bbox:
                cropped = image.crop(bbox)
                cropped.save(output_path)
                return output_path
            return image_path

        # === Step 3: Process Image ===
        def get_clean_product_cutout(input_photo_path):
            cutout_path = "product_cutout.png"
            cropped_path = "product_cutout_cropped.png"

            print("🧠 Removing background...")
            remove_background(input_photo_path, cutout_path)

            print("✂️ Cropping transparent edges...")
            autocrop_image(cutout_path, cropped_path)

            print(f"✅ Done! Final image saved at: {cropped_path}")
            final_garment_url = upload_image_to_azure(cropped_path, blob_name="garment")
            return final_garment_url

        # === RUN THIS ===
        garment_image_url = get_clean_product_cutout(garment_image)
        return JsonResponse({'image_url': garment_image_url})


@csrf_exempt
def upload_image(request):

    if request.method == 'POST':
        clothes_category = request.POST.get("category")
        
        model_image_file = request.FILES.get('model_image_file')  # newly uploaded file
        model_image_url = request.POST.get('model_image_url')     # existing image URL

        garment_image = request.FILES.get('garment_image')
        
        if not (model_image_file or model_image_url) or not garment_image:
            return JsonResponse({"error": "Both images are required."})

        
        # Compress & Upscale Start ---------------------------------------------->
        def compress_image(input_path, output_path, max_size_kb=1800, max_dimension=3000):
            
            # Check original file size
            original_size_kb = input_path.size / 1024

            # If already under the size limit, just copy or save without compression
            if original_size_kb <= max_size_kb:
                img = Image.open(input_path)
                img = ImageOps.exif_transpose(img)

                if img.mode in ("P", "RGBA"):
                    img = img.convert("RGB")

                img.save(output_path, optimize=True, quality=100)
                return  # Done, no compression needed

            # Otherwise, continue with resize + compression
            img = Image.open(input_path)
            img = ImageOps.exif_transpose(img)  # ✅ auto-rotate if needed

            if img.mode in ("P", "RGBA"):
                img = img.convert("RGB")

            if max(img.size) > max_dimension:
                img.thumbnail((max_dimension, max_dimension))

            quality = 100
            img.save(output_path, optimize=True, quality=quality)

            while os.path.getsize(output_path) > max_size_kb * 1024 and quality > 10:
                quality -= 2
                img.save(output_path, optimize=True, quality=quality)
        
        
        def upscale_image(input_path, output_path, scale_factor=6):
            """
            Upscale an image by the given scale_factor.
            """
            def open_image_from_url(image_url):
                response = requests.get(image_url)
                response.raise_for_status()  # raise error if request fails
                return Image.open(BytesIO(response.content))  # open image from memory

            img = open_image_from_url(input_path)  # where input_path is the HTTPS URL
            new_size = (img.width * scale_factor, img.height * scale_factor)
            upscaled_img = img.resize(new_size, Image.LANCZOS)
            upscaled_img.save(output_path)
            print("Upscaled")
                
        # Compress & Upscale End ---------------------------------------------->

        # Encode Image Start -------------------------------------------------------->
        def encode_image(image):
            return base64.b64encode(image.read()).decode('utf-8')
        # Encode Image End -------------------------------------------------------->

        # Resize Image Start -------------------------------------------------------->
        def resize_image(input_path, output_path):
            if input_path.startswith("http://") or input_path.startswith("https://"):
                response = requests.get(input_path)
                if response.status_code != 200:
                    raise ValueError("Failed to download image from URL")
                img = Image.open(BytesIO(response.content))
            else:
                img = Image.open(input_path)

            # Convert to RGB before saving as JPEG
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Step 1: Resize while maintaining aspect ratio (fit inside 768x1024)
            img.thumbnail((768, 1024), Image.LANCZOS)

            # Step 2: Create new image with desired size and white background
            background = Image.new('RGB', (768, 1024), (255, 255, 255))

            # Step 3: Center the resized image onto the background
            x = (768 - img.width) // 2
            y = (1024 - img.height) // 2
            background.paste(img, (x, y))

            # Step 4: Save with high quality
            background.save(output_path, format="JPEG", quality=100, optimize=False)

        # Resize Image End -------------------------------------------------------->
        
        # Compress
        compressed_path = os.path.join(MEDIA_ROOT, 'compressed-125.jpg')
        compress_image(garment_image, compressed_path)


        # Resize Image Start -------------------------------------------------------->
        resized_garment_path = os.path.join(MEDIA_ROOT, 'resized_garment_image.jpg')
        resize_image(compressed_path, resized_garment_path)

        # resized_model_path = os.path.join(MEDIA_ROOT, 'resized_model_image.jpg')
        # resize_image(model_image, resized_model_path)
        
        resized_model_path = os.path.join(MEDIA_ROOT, 'resized_model_image.jpg')

        if model_image_file:
            # Save the uploaded file temporarily to a path
            temp_model_path = os.path.join(MEDIA_ROOT, 'uploaded_model.jpg')
            with open(temp_model_path, 'wb+') as destination:
                for chunk in model_image_file.chunks():
                    destination.write(chunk)
            resize_image(temp_model_path, resized_model_path)
            os.remove(temp_model_path)  # optional: cleanup temp file
        else:
            resize_image(model_image_url, resized_model_path)

        # Resize Image End -------------------------------------------------------->

        # model_image_base64 = encode_image(model_image)
        # model_image_base64 = encode_image(garment_image)

        with open(resized_model_path, 'rb') as image_file:
            model_image_base64 = encode_image(image_file)

        with open(resized_garment_path, 'rb') as image_file:
            garment_image_base64 = encode_image(image_file)

        # with open(compressed_path, 'rb') as image_file:
        #     garment_image_base64 = encode_image(image_file)

        #     # Print file size
        #     file_size_kb = os.path.getsize(compressed_path) / 1024
        #     print(f"File size: {file_size_kb:.2f} KB")


        # # Open image to get dimensions
        # with Image.open(compressed_path) as img:
        #     width, height = img.size
        #     print(f"Image dimensions: {width} x {height} pixels")

        headers = {
            'X-API-Key': PINCEL_API_KEY,
            'Content-Type': 'application/json',
        }
        payload1 = {
            "model_image": f"data:image/jpeg;base64,{model_image_base64}",
            "garment_image": f"data:image/jpeg;base64,{garment_image_base64}",
            "category": clothes_category, 
            "action": "startPrediction"
        }
        try:
            response1 = requests.post(PINCEL_API_URL, json=payload1, headers=headers)
            data1 = response1.json()

            payload2 = {
                "predictionId": data1['prediction'],
                "action": "getPrediction"
            }
            while True:
                response2 = requests.post(PINCEL_API_URL, json=payload2, headers=headers)
                data2 = response2.json()

                if response2.status_code == 200:
                    status = data2.get('status')

                    if status == 'succeeded':
                        print("✅ Prediction completed! Image URL:", data2.get('output'))

                        def save_api_result_from_url(image_url, output_path):
                            response = requests.get(image_url)
                            if response.status_code == 200:
                                with open(output_path, 'wb') as f:
                                    f.write(response.content)
                            else:
                                print("Failed to download image. Status code:", response.status_code)



                        def get_next_filename(directory, prefix, extension):
                            # Ensure directory exists
                            if not os.path.exists(directory):
                                os.makedirs(directory)

                            existing_files = os.listdir(directory)
                            pattern = re.compile(rf"{re.escape(prefix)}-(\d+)\.{re.escape(extension)}")
                            numbers = [int(match.group(1)) for f in existing_files if (match := pattern.match(f))]
                            next_number = max(numbers) + 1 if numbers else 1
                            return f"{prefix}-{next_number}.{extension}"

                        # Set your subdirectory path
                        subdir = os.path.join(MEDIA_ROOT, 'upscaled')
                        filename = get_next_filename(subdir, 'final_upscaled', 'jpg')
                        upscaled_path = os.path.join(subdir, filename)
                        print("10")
                        print(filename)
                        # Save the Upscaled image
                        # upscale_image(data2.get('output'), upscaled_path)

                        # First Saving the Result
                        output_path = os.path.join(MEDIA_ROOT, 'api_result.jpg')
                        save_api_result_from_url(data2.get('output'), output_path)

                        try:
                            # Upload to Azure
                            upscaled_azure_url = upload_image_to_azure(output_path, blob_name="result")
                            print(upscaled_azure_url)
                            data2['upscaled_path'] = upscaled_azure_url
                        finally:
                            # Always clean up the local file
                            if os.path.exists(upscaled_path):
                                os.remove(upscaled_path)
                                os.remove(output_path)


                        # Add path to the response
                        # data2['upscaled_path'] = upscaled_azure_url

                        # Get the relative media URL from the file path
                        # relative_path = os.path.relpath(upscaled_path, MEDIA_ROOT)  # gives 'upscaled/final_upscaled-5.jpg'
                        # data2['upscaled_url'] = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, relative_path))

                        # relative_path = '/media/final_upscaled-125.jpg'
                        # data2['upscaled_url'] = request.build_absolute_uri(relative_path)

                        return JsonResponse(data2)
                    
                    elif status == 'failed':
                        print("❗ Prediction failed:", data2.get('error', 'Unknown error'))
                        return None
                    else:
                        print("⏳ Processing... Checking again in 5 seconds.")
                else:
                    print("❗ Error:", data2.get('error', 'Unknown error'))
                    return None

                time.sleep(5)  # Wait 5 seconds before checking again

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request"})


@csrf_exempt
def upscale_image(request):
    if request.method == 'POST':
        image_url = request.POST.get("image_url")

        if not image_url:
            return JsonResponse({"error": "No image URL provided."})

        headers = {
            "accept": "application/json",
            "X-Picsart-API-Key": PICSART_API_KEY
        }

        # ✅ Corrected: The Picsart API expects multipart/form-data.
        # Use a 'data' dictionary for your parameters.
        data_payload = {
            "image_url": image_url,
            "upscale_factor": "2"  # Note: The docs show 'upscale_factor' as a string like 'x2'.
                                  # Let's try sending it as a string to be safe.
        }
        
        api_url = "https://api.picsart.io/tools/1.0/upscale"

        # The 'requests' library automatically sets Content-Type to multipart/form-data
        # when you use the 'data' and/or 'files' parameters.
        response = requests.post(api_url, headers=headers, data=data_payload)

        try:
            result = response.json()

            if response.status_code == 200 and "url" in result["data"]:
                return JsonResponse({"upscaled_url": result["data"]["url"]})
            else:
                return JsonResponse({"error": result.get("error", "Unknown error from Picsart.")}, status=response.status_code)
        except Exception as e:
            return JsonResponse({"error": "Failed to parse response from Picsart."}, status=500)
    else:
        return JsonResponse({"error": "Only POST method allowed."}, status=405)



# @csrf_exempt
# def add_products(request):
#     valid = False
#     data = {}
#     if request.COOKIES.get('t'):
#         valid, data = verify_token(request.COOKIES['t'])
#     dashboard = None
#     if valid:
#         dashboard = 'dashboard'

#     user_type = data.get('user_type')
#     user_name = data.get('first_name')
#     user_email = data.get('email')
#     user_record = DB.users.find_one({"email": user_email})
#     users_shop_logo = user_record['shop_logo']
#     users_shop_address = user_record['shop_address']
#     users_shop_name = user_record['shop_name']
#     users_id = str(user_record['_id'])
#     credits = user_record.get("credits_used", 0)

#     print("✅ Add Product page started")

#     if request.method == 'POST':
#         try:
#             json_data1 = request.POST.get('document')
#             json_data2 = request.POST.get('selectedmiddlebuttons')
#             logger.debug("1. Received POST data.") # Using logger instead of print

#             if not json_data1:
#                 logger.error("❌ 'document' is missing in POST") # Using logger instead of print
#                 return JsonResponse({'error': 'Missing product data'}, status=400)

#             parsed_data1 = json.loads(json_data1)
#             parsed_data2 = json.loads(json_data2)

#             saved_garment_urls = []
#             saved_result_urls = []
#             logger.debug("2. Parsing data and initializing URL lists.") # Using logger instead of print

#             i = 0
#             while True:
#                 file_key1 = f'garment_{i}'
#                 uploaded_garment_file = request.FILES.get(file_key1)
#                 if not uploaded_garment_file:
#                     break
#                 uploaded_garment_url = upload_image_to_azure(uploaded_garment_file, blob_name="garment")
#                 saved_garment_urls.append(uploaded_garment_url)
#                 print("hi:-", saved_garment_urls)
#                 i += 1

#             index = 0
#             while True:
#                 file_key = f'result_file_{index}'
#                 url_key = f'result_url_{index}'

#                 if file_key in request.FILES:
#                     result_file = request.FILES[file_key]
#                     result_url = upload_image_to_azure(result_file, blob_name="result")
#                     saved_result_urls.append(result_url)
#                 elif url_key in request.POST:
#                     saved_result_urls.append(request.POST[url_key])
#                 else:
#                     break
#                 index += 1
#             logger.debug("3. Uploaded garment and result files to Azure Blob Storage.") # Using logger instead of print


#             # Extract plaintext data from parsed_data1 (received from frontend)
#             product_name = parsed_data1.get('product_name', 'Low Rise Wide Jeans')
#             product_fabric = parsed_data1.get('product_fabric', 'Cotton')
#             product_quantity = int(parsed_data1.get('product_quantity', 0))
            
#             # Renamed for clarity: These are the plaintext values coming from the frontend
#             product_price_plaintext = int(parsed_data1.get('product_price', 0))
#             product_selling_price_plaintext = int(parsed_data1.get('product_selling_price', 0))
            
#             sizes = parsed_data1.get('product_sizes', [])
#             product_colors = parsed_data1.get('product_colors', [])
#             brand_name = parsed_data1.get('brand_name', 'Unknown Brand')
#             qrcode_ids = parsed_data1.get('qrcode_ids', []) # Assuming this is a list of IDs

#             # Extract plaintext data from parsed_data2
#             category = parsed_data2.get('category', 'Jeans')
#             gender = parsed_data2.get('gender', 'Women')
#             subCategory = parsed_data2.get('subCategory', '')
#             finalCategory = parsed_data2.get('finalCategory', '')
#             swapCategory = parsed_data2.get('swapCategory', '')

#             # --- KMS ENCRYPTION FOR SENSITIVE DATA ---
#             # Convert integers to string, then to bytes for encryption
#             # try:
#             #     encrypted_product_bought_price = encrypt_with_kms(str(product_price_plaintext).encode('utf-8'))
#             #     encrypted_product_selling_price = encrypt_with_kms(str(product_selling_price_plaintext).encode('utf-8'))
#             #     logger.info("Product prices encrypted successfully using KMS.")
#             # except Exception as kms_e:
#             #     logger.critical(f"Failed to encrypt product prices with KMS: {kms_e}", exc_info=True)
#             #     # In production, it's critical to stop here if encryption fails.
#             #     return JsonResponse({'error': 'Failed to secure sensitive product data. Please try again or contact support.'}, status=500)


#             generated_urls=[]
#             generated_images = []
#             generated_colors = []

#             # Using plaintext selling price for calculations for social media/image generation
#             price_one_item = product_selling_price_plaintext 
#             len_variants = len(parsed_data1['product_colors'])
#             total_price = price_one_item * len_variants

#             # random_integer = random.randint(50, 150)
#             # upgraded_product_price = product_selling_price_plaintext + random_integer
#             # product_discount = int(((random_integer)/(upgraded_product_price)) * 100)


#             # logger.debug("6. Calculated prices and discounts.")
#             # logger.debug(f"Product details (plaintext from client): Name='{product_name}', Selling Price='{product_selling_price_plaintext}'")

#             variants = []
#             temp_files_to_cleanup = []

#             for i in range(len(parsed_data1['product_colors'])):
#                 garment_image_url = saved_garment_urls[i] if i < len(saved_garment_urls) else None
#                 result_image_url = saved_result_urls[i]

#                 decrypted_garment_image_io = None
#                 decrypted_result_image_io = None

#                 temp_result_image_path = None # Initialize temp paths for this iteration
#                 temp_garment_image_path = None

#                 try:
#                     # DOWNLOAD AND DECRYPT RESULT IMAGE FOR GENERATION
#                     if result_image_url:
#                         logger.info(f"Downloading and decrypting result image for variant {i}: {result_image_url}")
#                         decrypted_result_image_io = download_and_decrypt_image_from_azure(result_image_url)
                        
#                         # --- Save BytesIO to a temporary file ---
#                         with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
#                             tmp_file.write(decrypted_result_image_io.getvalue())
#                             temp_result_image_path = tmp_file.name
#                         logger.debug(f"Saved decrypted result image to temp file: {temp_result_image_path}")
#                         temp_files_to_cleanup.append(temp_result_image_path) # Add to list for cleanup

#                     # DOWNLOAD AND DECRYPT GARMENT IMAGE FOR GENERATION (if applicable)
#                     if garment_image_url:
#                         logger.info(f"Downloading and decrypting garment image for variant {i}: {garment_image_url}")
#                         decrypted_garment_image_io = download_and_decrypt_image_from_azure(garment_image_url)

#                         # --- Save BytesIO to a temporary file ---
#                         with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
#                             tmp_file.write(decrypted_garment_image_io.getvalue())
#                             temp_garment_image_path = tmp_file.name
#                         logger.debug(f"Saved decrypted garment image to temp file: {temp_garment_image_path}")
#                         temp_files_to_cleanup.append(temp_garment_image_path) # Add to list for cleanup

#                 except Exception as img_fetch_e:
#                     logger.error(f"Error downloading or decrypting image for generation (variant {i}): {img_fetch_e}", exc_info=True)
#                     # Ensure paths are None if an error occurs
#                     decrypted_garment_image_io = None
#                     decrypted_result_image_io = None
#                     temp_result_image_path = None
#                     temp_garment_image_path = None 


#                 variant = {
#                     "color": parsed_data1['product_colors'][i],
#                     "garment_image": garment_image_url, # Still store the original URL in DB
#                     "result_image": result_image_url,   # Still store the original URL in DB
#                 }
#                 variants.append(variant)

#                 output_path = "generated"
#                 texts = [
#                     f"ID: {parsed_data1['qrcode_ids'][0]}",
#                     f"Name: {product_name}",
#                     f"Price: ₹{parsed_data1['product_selling_price']}",
#                     f"Sizes: {parsed_data1['product_sizes']}",
#                     f"Fabric: {parsed_data1['product_fabric']}",
#                     f"Color: {parsed_data1['product_colors'][i]}"
#                 ]
#                 print("55")

#                 # --- PASS BytesIO OBJECTS TO IMAGE GENERATION FUNCTIONS ---
#                 # REMEMBER: Your create_offer_photo_with_right_image_2, create_dynamic_photo_with_auto_closeup_1/2
#                 # functions MUST be updated to accept io.BytesIO objects for image inputs.
#                 # Example: instead of `big_image_path='url'`, they should take `big_image_data=io.BytesIO(...)`.

#                 image_url_3 = create_offer_photo_with_right_image_2(
#                     big_image_path=temp_result_image_path, # Pass BytesIO object
#                     logo_path=users_shop_logo,         # Pass BytesIO object
#                     output_path="generated", # This remains as a logical path for Azure upload
#                     product_name=product_name,
#                     product_quantity=len_variants,
#                     product_selling_price_total_amount=total_price,
#                     product_id=parsed_data1['qrcode_ids'][0]
#                 )
#                 print("56")
#                 generated_urls.append(image_url_3)

#                 if decrypted_garment_image_io is None:
#                     azure_generated_image_url = create_dynamic_photo_with_auto_closeup_1(
#                         big_image_path=temp_result_image_path, # Pass BytesIO object
#                         logo_path=users_shop_logo,         # Pass BytesIO object
#                         texts=texts,
#                         output_path=output_path,
#                     )
#                 else:
#                     azure_generated_image_url = create_dynamic_photo_with_auto_closeup_2(
#                         big_image_path=temp_result_image_path,     # Pass BytesIO object
#                         logo_path=users_shop_logo,             # Pass BytesIO object
#                         texts=texts,
#                         output_path=output_path,
#                         garment_image_data=temp_garment_image_path # Pass BytesIO object
#                     )
#                 print("57")

#                 generated_images.append(azure_generated_image_url)
#                 generated_colors.append(parsed_data1['product_colors'][i])


#             def background_task_2():
#                 try:
#                     response1 = client.chat.completions.create(
#                         model="gpt-3.5-turbo",
#                         messages=[
#                             {
#                                 "role": "system",
#                                 "content": (
#                                     "You are a creative Instagram marketer who writes short, catchy, and trendy captions "
#                                     "for fashion products in India. Use emojis and 3–5 relevant fashion hashtags. "
#                                     "Keep the tone fun and engaging, and always be concise."
#                                 )
#                             },
#                             {
#                                 "role": "user",
#                                 "content": f"""
#                                     Generate an Instagram caption for the following fashion product carousel:

#                                     - 🛍️ Product Name: {product_name}  
#                                     - 👕 Category: {category}  
#                                     - 🧍 Gender: {gender}  
#                                     - 🧵 Fabric: {parsed_data1['product_fabric']}  
#                                     - 🎨 Available in {parsed_data1['product_quantity']} colors: {generated_colors}  
#                                     - 💰 Mega Deal: ₹{total_price} total (based on all variants)  

#                                     💡 Include this line in the caption:  
#                                     "To know more, enter the Product ID in the chat shown in the image!"  

#                                     📝 Caption Style:  
#                                     - Keep it short and attention-grabbing 
#                                     - Keep it simple and understandable as their english is not very good 
#                                     - Mention the discount/deal clearly  
#                                     - Use emojis and make it carousel-appropriate  
#                                     - Add 3–5 trendy fashion hashtags at the end
#                                 """
#                             }
#                         ]
#                     )
#                     reply1 = response1.choices[0].message.content
#                     if len(generated_urls) > 1:
#                         print_response1 = post_carousel_to_instagram(generated_urls, reply1)
#                         logger.info(f"response-1 (carousel): {print_response1}")
#                     else:
#                         print_response1 = post_to_instagram(generated_urls, reply1)
#                         logger.info(f"response-1 (single post): {print_response1}")
#                 except Exception as e:
#                     logger.error(f"Error in background_task_2 (Instagram posting/GPT): {e}", exc_info=True)
            
#             thread2 = threading.Thread(target=background_task_2)
#             thread2.daemon = True
#             thread2.start()

#             logger.info("[INFO] Instagram posting thread-2 started.")
                
            
#             image_dict = {
#                 "user_id": users_id,
#                 "qr_ids": parsed_data1['qrcode_ids'],
#                 "image_urls": generated_images,
#                 "is_downloaded": False,
#                 "created_at": localtime(timezone.now()).strftime("%d-%m-%Y")
#             }

#             DB.images_download.insert_one(image_dict)

#             # Video Generation by Threading Starts ---------------->
#             video_url = ''
#             video_groups = []

#             product_entry = {
#                 "clothes_category": category,
#                 "gender": gender,
#                 "product_selling_price": product_selling_price_plaintext, # Using plaintext for video generation for now
#                 "product_name": product_name,
#                 "image_urls": generated_urls
#             }

#             video_groups.append(product_entry)

#             video_dict = {
#                 "user_id": users_id,
#                 "qr_ids": parsed_data1['qrcode_ids'],
#                 "video_urls": video_url,
#                 "video_groups": video_groups,
#                 "video_generated": False,
#                 "is_downloaded": False,
#                 "created_at": localtime(timezone.now()).strftime("%d-%m-%Y")
#             }

#             DB.videos_download.insert_one(video_dict)

#             video_records = list(DB.videos_download.find( # Changed from DB.videos_downloaded.find to DB.videos_download.find
#                 {"user_id": users_id, "video_generated": False}
#             ))

#             video_groups_for_gen = [] # Renamed to avoid conflict and be clearer
#             product_info = [] # This variable still seems unused/empty as passed to start_video_generation_2

#             for record in video_records:
#                 groups = record.get("video_groups", [])
#                 for group in groups:
#                     product_name_video = group.get("product_name")
#                     image_urls_video = group.get("image_urls")
#                     video_groups_for_gen.append({"product_name": product_name_video, "image_urls": image_urls_video})

#             total_images = sum(len(group["image_urls"]) for group in video_groups_for_gen)

#             if total_images >= 8:
#                 video_output_path = f"output/generated_reel_{uuid.uuid4().hex}.mp4"
#                 logger.debug("Initiating video generation for enough images.")

#                 def background_task():
#                     try:
#                         video_url_generated = start_video_generation_2(video_groups_for_gen, video_output_path, users_shop_address, users_shop_name, product_info)
                        
#                         response2 = client.chat.completions.create(
#                             model="gpt-3.5-turbo",
#                             messages=[
#                                 {"role": "system", "content": "You are a creative Instagram marketer who writes short, catchy, and trendy captions for fashion products in India. Use emojis and hashtags where relevant. And be concise."},
#                                 {
#                                     "role": "user",
#                                     "content": """Generate an Instagram caption for a product video that shows different fashion styles and variants.

#                                     Tell users that:
#                                     - New styles just dropped
#                                     - To DM the product ID shown in the video to know more
#                                     - Prices range from ₹200 to ₹700
#                                     - Add excitement with phrases like Mega Deal or Limited Stock
#                                     - Add 3–5 trendy fashion hashtags at the end

#                                     Keep the tone casual, exciting, and attention-grabbing."""
#                                 }
#                             ]
#                         )

#                         reply_2 = response2.choices[0].message.content
                        
#                         result = post_azure_video_to_instagram(video_url_generated, reply_2)
#                         logger.info(f"response-2 (video post): {result}")

#                         if video_url_generated:
#                             # Update all records for this user that are not yet generated
#                             DB.videos_download.update_many( # Changed to update_many if qr_ids not unique for the record
#                                 {"user_id": users_id, "video_generated": False},
#                                 {'$set': 
#                                     {
#                                         "video_urls": video_url_generated,
#                                         "video_generated": True,
#                                         # image_urls might be more appropriate to update on initial insert, not here
#                                         # "image_urls": generated_urls, 
#                                     }
#                                 }
#                             )
#                     except Exception as e:
#                         logger.error(f"Error in background_task (video generation/Instagram): {e}", exc_info=True)

#                 thread = threading.Thread(target=background_task)
#                 thread.daemon = True
#                 thread.start()

#                 logger.info("[INFO] Video generation thread-1 started.")


#             # Final DB insert for the product itself
#             products_dict = {
#                 "user_id": users_id,
#                 "qrcode_ids": parsed_data1['qrcode_ids'],
#                 "product_gender": parsed_data2['gender'],
#                 "product_category": parsed_data2['category'],
#                 "product_subCategory": parsed_data2['subCategory'],
#                 "product_finalCategory": parsed_data2['finalCategory'],
#                 "product_swapCategory": parsed_data2['swapCategory'],
#                 "brand_name": brand_name,
#                 "product_name": product_name,
#                 "product_fabric": product_fabric,
#                 "sets_available": product_quantity,
#                 "sizes": sizes,
#                 "product_bought_price": encrypted_product_bought_price, # <-- ENCRYPTED
#                 "product_selling_price": encrypted_product_selling_price, # <-- ENCRYPTED
#                 "variants": variants,
#                 "created_on": localtime(timezone.now())
#             }

#             DB.products.insert_one(products_dict)
#             logger.info("✅ Product inserted successfully into DB.")

#             return JsonResponse({'uploaded_urls': "uploaded"})

#         except Exception as e:
#             logger.critical(f"❌ Unhandled Exception in add_products view: {e}", exc_info=True)
#             return JsonResponse({'error': 'Something went wrong', 'details': str(e)}, status=500)

#     return render(request, 'add_products.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, 'credits': credits})


@csrf_exempt
def add_products(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    user_email = data.get('email')
    user_record = DB.users.find_one({"email": user_email})
    users_shop_logo = user_record['shop_logo']
    users_shop_address = user_record['shop_address']
    users_shop_name = user_record['shop_name']
    users_id = str(user_record['_id'])

    credits = user_record.get("credits_used", 0)

    print("✅ Add Product page started")

    if request.method == 'POST':
        try:

            # ✅ Safely get the data sent as FormData
            json_data1 = request.POST.get('document')
            json_data2 = request.POST.get('selectedmiddlebuttons')
            logger.debug("1. Received POST data.") # Using logger instead of print
            print("1")

            if not json_data1:
                logger.error("❌ 'document' is missing in POST") # Using logger instead of print
                return JsonResponse({'error': 'Missing product data'}, status=400)

            parsed_data1 = json.loads(json_data1)
            parsed_data2 = json.loads(json_data2)

            print("2")

            # Prepare to save uploaded garment images
            saved_garment_urls = []
            saved_result_urls = []

            i = 0
            while True:
                file_key1 = f'garment_{i}'
                uploaded_garment_file = request.FILES.get(file_key1)
                if not uploaded_garment_file:
                    break

                uploaded_garment_url = upload_image_to_azure(uploaded_garment_file, blob_name="garment")
                saved_garment_urls.append(uploaded_garment_url)
                i += 1

            # Handle result images (mixed types)
            index = 0
            while True:
                file_key = f'result_file_{index}'
                url_key = f'result_url_{index}'

                if file_key in request.FILES:
                    result_file = request.FILES[file_key]
                    result_url = upload_image_to_azure(result_file, blob_name="result")
                    saved_result_urls.append(result_url)
                elif url_key in request.POST:
                    saved_result_urls.append(request.POST[url_key])
                else:
                    break  # Stop when no more result_x keys found
                index += 1

            print("3")

            generated_urls=[]
            generated_images = []
            generated_colors = []

            product_name = parsed_data1.get('product_name', 'Low Rise Wide Jeans')
            category = parsed_data2.get('category', 'Jeans')
            gender = parsed_data2.get('gender', 'Women')

            price_one_item = int(parsed_data1.get('product_selling_price', '0'))
            len_variants = len(parsed_data1['product_colors'])
            total_price = price_one_item * len_variants

            # random_integer = random.randint(50, 150)
            # upgraded_product_price = int(parsed_data1['product_selling_price']) + random_integer
            # product_discount = int(((random_integer)/(upgraded_product_price)) * 100)

            # Build the variants array
            variants = []
            for i in range(len(parsed_data1['product_colors'])):
                garment_image = saved_garment_urls[i] if i < len(saved_garment_urls) else None
                variant = {
                    "color": parsed_data1['product_colors'][i],
                    "garment_image": garment_image,
                    "result_image": saved_result_urls[i],
                }
                variants.append(variant)

                # For Image Generation with Text
                big_image_path = saved_result_urls[i]
                garment_image_path = garment_image
                logo_path = users_shop_logo
                output_path = "generated"
                texts = [
                    f"ID: {parsed_data1['qrcode_ids'][0]}",
                    f"Name: {product_name}",
                    f"Price: ₹{parsed_data1['product_selling_price']}",
                    f"Sizes: {parsed_data1['product_sizes']}",
                    f"Fabric: {parsed_data1['product_fabric']}",
                    f"Color: {parsed_data1['product_colors'][i]}"
                ]
                # image_url_2 = create_offer_photo_with_right_image(
                #     big_image_path=big_image_path,
                #     output_path="generated",
                #     product_id=parsed_data1['qrcode_ids'][0],
                #     offer_title="Mega Deal",
                #     discount_text=f"{product_discount}% OFF",
                #     final_line_1="DM the Product Id to",
                #     final_line_2="Know more."
                # )
                image_url_3 = create_offer_photo_with_right_image_2(
                    big_image_path=big_image_path,
                    logo_path=logo_path,
                    output_path="generated",
                    product_name=product_name,
                    product_quantity=len_variants,
                    product_selling_price_total_amount=total_price,
                    product_id=parsed_data1['qrcode_ids'][0]
                )
                generated_urls.append(image_url_3)

                if garment_image is None:
                    azure_generated_image_url = create_dynamic_photo_with_auto_closeup_1(
                    big_image_path=big_image_path,
                    logo_path=logo_path,
                    texts=texts,
                    output_path=output_path,
                ) 
                else:
                    azure_generated_image_url = create_dynamic_photo_with_auto_closeup_2(
                        big_image_path=big_image_path,
                        logo_path=logo_path,
                        texts=texts,
                        output_path=output_path,
                        garment_image_path=garment_image_path
                    )

                generated_images.append(azure_generated_image_url)

                generated_colors.append(parsed_data1['product_colors'][i])

            def background_task_2():
                try:

                    response1 = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are a creative Instagram marketer who writes short, catchy, and trendy captions "
                                    "for fashion products in India. Use emojis and 3–5 relevant fashion hashtags. "
                                    "Keep the tone fun and engaging, and always be concise."
                                )
                            },
                            {
                                "role": "user",
                                "content": f"""
                                    Generate an Instagram caption for the following fashion product carousel:

                                    - 🛍️ Product Name: {product_name}  
                                    - 👕 Category: {category}  
                                    - 🧍 Gender: {gender}  
                                    - 🧵 Fabric: {parsed_data1['product_fabric']}  
                                    - 🎨 Available in {parsed_data1['product_quantity']} colors: {generated_colors}  
                                    - 💰 Mega Deal: ₹{total_price} total (based on all variants)  

                                    💡 Include this line in the caption:  
                                    "To know more, enter the Product ID in the chat shown in the image!"  

                                    📝 Caption Style:  
                                    - Keep it short and attention-grabbing 
                                    - Keep it simple and understandable as their english is not very good 
                                    - Mention the discount/deal clearly  
                                    - Use emojis and make it carousel-appropriate  
                                    - Add 3–5 trendy fashion hashtags at the end
                                """
                            }
                        ]
                    )
                    reply1 = response1.choices[0].message.content
                    if len(generated_urls) > 1:
                        print_response1 = post_carousel_to_instagram(generated_urls, reply1)
                    else:
                        print_response1 = post_to_instagram(generated_urls, reply1)

                except Exception as e:
                    logger.error(f"Error in background_task_2 (Instagram posting/GPT): {e}", exc_info=True)
                
            thread2 = threading.Thread(target=background_task_2)
            thread2.daemon = True
            thread2.start()

            logger.info("[INFO] Instagram posting thread-2 started.")
            
            image_dict = {
                "user_id": users_id,
                "qr_ids": parsed_data1['qrcode_ids'],
                "image_urls": generated_images,
                "is_downloaded": False,
                "created_at": localtime(timezone.now()).strftime("%d-%m-%Y")
            }

            DB.images_download.insert_one(image_dict)

            # Video Generation by Threading Starts ---------------->
            video_url = ''
            video_groups = []

            product_entry = {
                "clothes_category": category,
                "gender": gender,
                "product_selling_price": parsed_data1['product_selling_price'],
                "product_name": product_name,
                "image_urls": saved_result_urls
            }

            video_groups.append(product_entry)

            video_dict = {
                "user_id": users_id,
                "qr_ids": parsed_data1['qrcode_ids'],
                "video_urls": video_url,
                "video_groups": video_groups,
                "video_generated": False,
                "is_downloaded": False,
                "created_at": localtime(timezone.now()).strftime("%d-%m-%Y")
            }

            DB.videos_download.insert_one(video_dict)

            video_groups = []
            product_info = []

            video_records = list(DB.videos_download.find(
                {"user_id": users_id, "video_generated": False}
            ))

            for record in video_records:
                groups = record.get("video_groups", [])
                for group in groups:
                    product_name = group.get("product_name")
                    image_urls = group.get("image_urls")
                    video_groups.append({"product_name": product_name, "image_urls": image_urls})

            total_images = sum(len(group["image_urls"]) for group in video_groups)

            if total_images >= 4:
                video_output_path = f"output/generated_reel_{uuid.uuid4().hex}.mp4"
                logger.debug("Initiating video generation for enough images.")

                # SAFETY: Start thread and don't store the thread object
                def background_task():
                    try:
                        video_url = start_video_generation_2(video_groups, video_output_path, users_shop_address, users_shop_name)
                        
                        response2 = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a creative Instagram marketer who writes short, catchy, and trendy captions for fashion products in India. Use emojis and hashtags where relevant. And be concise."},
                                {
                                    "role": "user",
                                    "content": """Generate an Instagram caption for a product video that shows different fashion styles and variants.

                                    Tell users that:
                                    - New styles just dropped
                                    - To DM the product ID shown in the video to know more
                                    - Prices range from ₹200 to ₹700
                                    - Add excitement with phrases like Mega Deal or Limited Stock
                                    - Add 3–5 trendy fashion hashtags at the end

                                    Keep the tone casual, exciting, and attention-grabbing."""
                                }
                            ]
                        )

                        reply_2 = response2.choices[0].message.content
                        
                        result = post_azure_video_to_instagram(video_url, reply_2)
                        logger.info(f"response-2 (video post): {result}")

                        if video_url:
                            DB.videos_download.update_many(
                                {"user_id": users_id, "video_generated": False},
                                {'$set': 
                                    {
                                        "video_urls": video_url,
                                        "video_generated": True,
                                    }
                                }
                            )
                    except Exception as e:
                        logger.error(f"Error in background_task (video generation/Instagram): {e}", exc_info=True)

                thread = threading.Thread(target=background_task)
                thread.daemon = True
                thread.start()

                logger.info("[INFO] Video generation thread-1 started.")


            products_dict = {
                "user_id": users_id,
                "qrcode_ids": parsed_data1['qrcode_ids'],
                "product_gender": parsed_data2['gender'],
                "product_category": parsed_data2['category'],
                "product_subCategory": parsed_data2['subCategory'],
                "product_finalCategory": parsed_data2['finalCategory'],
                "product_swapCategory": parsed_data2['swapCategory'],
                "brand_name": parsed_data1['brand_name'],
                "product_name": parsed_data1['product_name'],
                "product_fabric": parsed_data1['product_fabric'],
                "sets_available": int(parsed_data1['product_quantity']),
                "sizes": parsed_data1['product_sizes'],
                "product_bought_price": parsed_data1['product_price'],
                "product_selling_price": parsed_data1['product_selling_price'],
                "variants": variants,
                "created_on": localtime(timezone.now())

            }
            # DB.products.create_index({"qrcode_ids": 1})

            DB.products.insert_one(products_dict)
            logger.info("✅ Product inserted successfully into DB.")

            return JsonResponse({'uploaded_urls': "uploaded"})

        except Exception as e:
            logger.critical(f"❌ Unhandled Exception in add_products view: {e}", exc_info=True)
            return JsonResponse({'error': 'Something went wrong', 'details': str(e)}, status=500)
            

    return render(request, 'add_products.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, 'credits': credits})



@csrf_exempt
def add_products_2(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'

    user_type = data.get('user_type')
    user_email = data.get('email')
    user_name = data.get('first_name')
    user_doc = DB.users.find_one({"email": user_email})
    users_shop_logo = user_doc.get('shop_logo', '')
    user_id = str(user_doc["_id"])

    if request.method == 'POST':
        try:
            # ===== Collect fields first (safe to pass to thread) =====
            product_name = request.POST.get("product_name")
            product_id = request.POST.get("product_id")
            fabric = request.POST.get("fabric")
            sizes = request.POST.get("sizes")
            selling_price = request.POST.get("selling_price")
            dupatta_side = request.POST.get("dupatta_side")

            # ===== Read file bytes immediately =====
            main_image_file = request.FILES.get('main_image')
            main_image_bytes = main_image_file.read() if main_image_file else None

            all_colors_single_file = request.FILES.get('all_colors_single')
            all_colors_single_bytes = all_colors_single_file.read() if all_colors_single_file else None

            color_images_files = list(request.FILES.getlist('color_images[]'))
            color_images_bytes = [f.read() for f in color_images_files]

            embroidery_files = list(request.FILES.getlist('embroidery_images[]'))
            embroidery_bytes_list = [f.read() for f in embroidery_files]

            embroidery_parts = list(request.POST.getlist('embroidery_parts[]'))

            # ===== Background Task =====
            def background_task():
                try:
                    # def file_to_base64(image_bytes):
                    #     return "data:image/png;base64," + base64.b64encode(image_bytes).decode("utf-8")

                    # # Step 1: Garment description
                    # def generate_garment_prompt(image_b64):
                    #     response = client.chat.completions.create(
                    #         model="gpt-4o-mini",
                    #         messages=[
                    #             {
                    #                 "role": "user",
                    #                 "content": [
                    #                     {
                    #                         "type": "text",
                    #                         "text": (
                    #                             "Describe this garment clearly in a short paragraph. "
                    #                             "Focus on garment type, fabric, structure, silhouette, length, "
                    #                             "design elements, colors, and overall fashion style. "
                    #                             "Keep it natural, keyword-rich, and not overly detailed."
                    #                         ),
                    #                     },
                    #                     {"type": "image_url", "image_url": {"url": image_b64}},
                    #                 ],
                    #             }
                    #         ],
                    #     )
                    #     return response.choices[0].message.content.strip()

                    # # Step 2: Embroidery details
                    # def generate_embroidery_prompt(image_b64, part):
                    #     response = client.chat.completions.create(
                    #         model="gpt-4o-mini",
                    #         messages=[
                    #             {
                    #                 "role": "user",
                    #                 "content": [
                    #                     {
                    #                         "type": "text",
                    #                         "text": (
                    #                             f"Describe the embroidery work specifically for the garment part: {part}. "
                    #                             "Provide detailed bullet points. Do NOT summarize or shorten. "
                    #                             "Focus on: stitching technique, thread type, colors, motifs, patterns, "
                    #                             "placement on garment, and texture. "
                    #                             "Explicitly mention if there are rectangular panels, floral motifs, "
                    #                             "geometric designs, neckline concentration, or scattered motifs. "
                    #                             "Be as specific and descriptive as possible, keeping accuracy >95%."
                    #                         ),
                    #                     },
                    #                     {"type": "image_url", "image_url": {"url": image_b64}},
                    #                 ],
                    #             }
                    #         ],
                    #     )
                    #     description = response.choices[0].message.content.strip()
                    #     return f"### {part} Embroidery\n\n{description}"

                    # --- Handle Images ---
                    saved_main_image_url = None
                    saved_all_colors_single_url = None
                    # garment_prompt = None

                    if main_image_bytes:
                        main_image_io = BytesIO(main_image_bytes)
                        main_image_io.name = "main_image.png"
                        saved_main_image_url = upload_image_to_azure(main_image_io, blob_name="garment")
                        # main_image_b64 = file_to_base64(main_image_bytes)
                        # garment_prompt = generate_garment_prompt(main_image_b64)

                    if all_colors_single_bytes:
                        all_colors_io = BytesIO(all_colors_single_bytes)
                        all_colors_io.name = "all_colors.png"
                        saved_all_colors_single_url = upload_image_to_azure(all_colors_io, blob_name="garment")

                    color_images_urls = []
                    for idx, img_bytes in enumerate(color_images_bytes):
                        img_io = BytesIO(img_bytes)
                        img_io.name = f"color_{idx}.png"
                        img_obj = Image.open(img_io).convert("RGBA")
                        temp_bytes = BytesIO()
                        img_obj.save(temp_bytes, format='PNG')
                        temp_bytes.seek(0)
                        azure_url = upload_image_to_azure(temp_bytes, blob_name="tempfiles")
                        color_images_urls.append(azure_url)

                    collage_url = create_collage(color_images_urls, users_shop_logo)

                    # === Embroidery Images with parts ===
                    embroidery_data = []
                    for idx, emb_bytes in enumerate(embroidery_bytes_list):
                        try:
                            part = embroidery_parts[idx] if idx < len(embroidery_parts) else None
                            if not part:
                                continue

                            emb_io = BytesIO(emb_bytes)
                            emb_io.name = f"embroidery_{idx}.png"
                            azure_url = upload_image_to_azure(emb_io, blob_name="tempfiles")
                            # embroidery_b64 = file_to_base64(emb_bytes)
                            # embroidery_prompt = generate_embroidery_prompt(embroidery_b64, part)

                            embroidery_data.append({
                                "url": azure_url,
                                "part": part,
                                # "description": embroidery_prompt
                            })
                        except Exception as e:
                            logger.error(f"❌ Failed to process embroidery image {idx}: {e}")

                    # Final Prompt
                    final_prompt = (
                        "I am sending you the ladies suit mannequin image and secondi image is the top kurti embroidery part. The top kurti neckline embroidery part should be exactly same, no changes, no adding any stuff. Generate a full-body image of a beautiful South Asian Nepali female model with fair skin, natural features, and an elegant look. She should have a confident smile, standing naturally on the ground in front of a Nepal tourist destination background. Her size must be proportionate to the background (not larger than the location). Make the image high-resolution, photorealistic, and best quality, so the fabric textures, embroidery threads, and model’s features appear sharp, realistic, and detailed. It should look real, and give best quality image. - and I am giving 2 images one mannequin and one embroidery neckline closeup."
                    )
                    # base_instruction = (
                    #     f"Create a tall Female with white skin, wearing {product_name}. "
                    #     f"- Dupatta on {dupatta_side}\n"
                    #     "- Place model in an elegant decor background\n"
                    #     "- Render in high quality, full body\n\n"
                    # )

                    # embroidery_descriptions = ""
                    # if embroidery_data:
                    #     embroidery_descriptions = "### Embroidery Details:\n"
                    #     for e in embroidery_data:
                    #         embroidery_descriptions += f"**{e['part']} Embroidery:**\n{e['description'].strip()}\n\n"

                    # if garment_prompt and embroidery_descriptions:
                    #     final_prompt = (
                    #         base_instruction
                    #         + "### Garment Details:\n"
                    #         + garment_prompt.strip()
                    #         + "\n\n### Embroidery Details:\n"
                    #         + embroidery_descriptions.strip()
                    #     )
                    # elif garment_prompt:
                    #     final_prompt = base_instruction + "### Garment Details:\n" + garment_prompt.strip()
                    # elif embroidery_descriptions:
                    #     final_prompt = base_instruction + "### Embroidery Details:\n" + embroidery_descriptions.strip()
                    # else:
                    #     final_prompt = base_instruction + "No garment details available."

                    # Insert into DB
                    product_dict = {
                        "product_name": product_name,
                        "product_id": product_id,
                        "fabric": fabric,
                        "sizes": sizes,
                        "selling_price": selling_price,
                        "dupatta_side": dupatta_side,
                        "prompt": final_prompt,
                        "dummy_image": saved_main_image_url,
                        "all_colors_image": saved_all_colors_single_url,
                        "Multiple_colors_image": color_images_urls,
                        "collage_image": collage_url,
                        "embroidery": embroidery_data,
                        "user_id": user_id
                    }

                    DB.products_2.insert_one(product_dict)
                    logger.info("✅ Product inserted successfully into DB (background).")

                except Exception as e:
                    logger.critical(f"❌ Unhandled Exception in background_task: {e}", exc_info=True)

            # ===== Launch background thread =====
            thread = threading.Thread(target=background_task)
            thread.daemon = True
            thread.start()

            # ===== Respond immediately =====
            return JsonResponse({
                'status': 'processing',
                'message': f'Product {product_name} is being processed in background'
            })

        except Exception as e:
            logger.critical(f"❌ Unhandled Exception in add_products_2: {e}", exc_info=True)
            return JsonResponse({'error': 'Something went wrong', 'details': str(e)}, status=500)

    else:
        return render(request, "add_products_2.html", {
            "dashboard": dashboard,
            "user_type": user_type,
            "first_name": user_name
        })


def in_stock_products(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'

    user_type = data.get('user_type')
    user_name = data.get('first_name')

    user_email = data.get('email')
    user_record = DB.users.find_one({"email": user_email})

    users_shop_name = user_record['shop_name']
    shop_name = users_shop_name.lower().replace(" ", "-")

    users_id = str(user_record['_id'])

    # # 🔐 Prepare AES key using user's password and salt
    # encryption_salt = request.session.get('encryptionSalt', user_email)
    # aes_key_bytes = derive_aes_key(user_record['password'], encryption_salt)

    products = list(DB.products.find({"user_id": users_id}).sort("sets_available", 1))
    for p in products:
        p["_id"] = str(p["_id"])
        p["id"] = p["_id"]
        print(f"Product ID in view:", p["_id"])

    # for p in products:
    #     p["_id"] = str(p["_id"])

    #     # 🔓 Decrypt sensitive fields
    #     p["product_name"] = decrypt_field_if_needed(p.get("product_name", ""), aes_key_bytes)
    #     p["product_fabric"] = decrypt_field_if_needed(p.get("product_fabric", ""), aes_key_bytes)
    #     p["sizes"] = decrypt_field_if_needed(p.get("sizes", ""), aes_key_bytes)

    #     # Variants is a list of dicts
    #     for variant in p.get("variants", []):
    #         variant["color"] = decrypt_field_if_needed(variant.get("color", ""), aes_key_bytes)
    #         variant["garment_image"] = decrypt_field_if_needed(variant.get("garment_image", ""), aes_key_bytes)
    #         variant["result_image"] = decrypt_field_if_needed(variant.get("result_image", ""), aes_key_bytes)

    return render(request, 'in_stock.html',  {
        'dashboard': dashboard,
        'user_type': user_type,
        'first_name': user_name,
        'shop_name': shop_name,
        'users_id': users_id,
        "products": products
    })


def in_stock_products_2(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'

    user_type = data.get('user_type')
    user_name = data.get('first_name')

    user_email = data.get('email')
    user_record = DB.users.find_one({"email": user_email})

    users_shop_name = user_record['shop_name']
    shop_name = users_shop_name.lower().replace(" ", "-")

    users_id = str(user_record['_id'])

    products = list(
        DB.products_2.find({"user_id": users_id}).sort("_id", -1)  # newest first
    )

    for p in products:
        p["_id"] = str(p["_id"])
        p["id"] = p["_id"]

    return render(request, 'in_stock_2.html',  {
        'dashboard': dashboard,
        'user_type': user_type,
        'first_name': user_name,
        'shop_name': shop_name,
        'users_id': users_id,
        "products": products
    })


@csrf_exempt
def update_instock_2(request, product_id):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    if not valid:
        return redirect("/login")
    
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    # fetch product
    product = DB.products_2.find_one({"_id": ObjectId(product_id)})
    if not product:
        return HttpResponse("Product not found", status=404)

    # fetch shop logo if you need for collage
    user_email = data.get('email')
    user_record = DB.users.find_one({"email": user_email})
    users_shop_logo = user_record.get("shop_logo") if user_record else None

    if request.method == "POST":
        # get uploaded files
        color_images_files = list(request.FILES.getlist("images"))

        color_images_bytes = [f.read() for f in color_images_files]
        color_images_urls = []

        for idx, img_bytes in enumerate(color_images_bytes):
            img_io = BytesIO(img_bytes)
            img_io.name = f"color_{idx}.png"

            # convert to PNG
            img_obj = Image.open(img_io).convert("RGBA")
            temp_bytes = BytesIO()
            img_obj.save(temp_bytes, format="PNG")
            temp_bytes.seek(0)

            # upload to Azure
            azure_url = upload_image_to_azure(temp_bytes, blob_name="tempfiles")
            color_images_urls.append(azure_url)

        # create collage if needed
        collage_url = create_collage(color_images_urls, users_shop_logo)

        # update DB: save both multiple image URLs & collage
        DB.products_2.update_one(
            {"_id": ObjectId(product_id)},
            {
                "$set": {
                    "collage_image": collage_url  # overwrite single collage field too
                }
            }
        )

        return redirect("in_stock_products_2")

    product["_id"] = str(product["_id"])
    return render(request, 'update_instock_2.html',  {
        'dashboard': dashboard,
        'user_type': user_type,
        'first_name': user_name,
        "product": product
    })

    

def products_sold_view(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'

    user_type = data.get('user_type')
    user_name = data.get('first_name')
    user_email = data.get('email')

    user_record = DB.users.find_one({"email": user_email})
    users_id = str(user_record['_id'])

    try:
        raw_sales = list(DB.products_sold.find({"user_id": users_id}))

        # ✅ Sort manually by sold_on timestamp (CosmosDB-safe)
        def extract_timestamp(sold_on):
            try:
                if isinstance(sold_on, dict) and "$date" in sold_on:
                    return int(sold_on["$date"])
                elif isinstance(sold_on, (int, float)):
                    return int(sold_on)
                elif isinstance(sold_on, datetime):
                    return int(sold_on.timestamp() * 1000)
            except Exception as e:
                print("❌ extract_timestamp error:", e)
            return 0  # fallback

        raw_sales.sort(key=lambda x: extract_timestamp(x.get("sold_on")), reverse=True)

        rows = []
        for invoice in raw_sales:
            sold_date = invoice.get("sold_on")
            formatted_date = ""

            try:
                if isinstance(sold_date, datetime):
                    formatted_date = sold_date.strftime("%d-%m-%Y")
                elif isinstance(sold_date, dict) and "$date" in sold_date:
                    timestamp_ms = sold_date["$date"]
                    if isinstance(timestamp_ms, (int, float)):
                        sold_date_obj = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
                        formatted_date = sold_date_obj.strftime("%d-%m-%Y")
                elif isinstance(sold_date, (int, float)):
                    sold_date_obj = datetime.fromtimestamp(sold_date / 1000, tz=timezone.utc)
                    formatted_date = sold_date_obj.strftime("%d-%m-%Y")
            except Exception as e:
                print("❌ Error parsing sold_on:", sold_date, e)
                formatted_date = ""

            # === Group products by product_id in the same invoice ===
            grouped_products = {}
            total_products_sold = 0


            for product in invoice.get("products", []):
                pid = product.get("product_id")

                grouped_products[pid] = {
                    "invoice_id": invoice.get("invoice_id"),
                    "product_id": pid,
                    "product_name": product.get("product_name"),
                    "qrcode_id": product.get("qrcode_ids"),
                    "quantity": product.get("sets_size"),
                    "price_per_item": product.get("price_per_item"),
                    "total_price": invoice.get("total_amount"),
                    "sold_on": formatted_date
                }

            rows.extend(grouped_products.values())

        return render(request, 'products_sold.html', {
            'dashboard': dashboard,
            'user_type': user_type,
            'first_name': user_name,
            "sold_rows": rows
        })

    except Exception as e:
        logger.error("❌ Failed in products_sold_view: %s", str(e))
        return render(request, 'add_products.html', {'error_message': 'Something went wrong loading your sales data.'})


@csrf_exempt
def exchange(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    # Get all exchange data sorted by date
    all_data = list(DB.exchange.find())
    for doc in all_data:
        doc["_id"] = str(doc["_id"])  # Make serializable

    # Optional: sort by date
    all_data.sort(key=lambda x: x["date"])

    # return JsonResponse({"exchange_data": all_data})

    print("✅ Exchange Product page started")

    if request.method == "POST":
        try: 
            print("1")
            data = json.loads(request.body)
            scanned_data = data.get("data", {})
            print(scanned_data)
            
            for qr_id in scanned_data["qr_ids"]:
                exchange_data = DB.exchange.find_one({"qr_id": qr_id})
                if not exchange_data:
                    product = DB.products.find_one({"qrcode_ids": qr_id})
                    if product:
                        exchange_dict = {
                            "qr_id": qr_id,
                            "date": localtime(timezone.now()).strftime("%d-%m-%Y"),
                            "product_name": product.get("product_name", "N/A"),
                            "status": scanned_data.get("status"),
                        }
                        DB.exchange.insert_one(exchange_dict)

                        if (scanned_data.get("status") == "Returned"):
                            DB.products.update_one(
                                {"qrcode_ids": qr_id},
                                {
                                    "$inc": {"sets_available": -1},
                                    "$pull": {"qrcode_ids": qr_id}
                                }
                            )
                        elif (scanned_data.get("status") == "Deleted"):
                            DB.prodcuts.delete_one({"qrcode_ids": qr_id})

            
            print("3")
            
            all_data2 = list(DB.exchange.find())
            for doc in all_data2:
                doc["_id"] = str(doc["_id"])  # Make serializable

            # Optional: sort by date
            all_data2.sort(key=lambda x: x["date"])
            print(all_data2)

            return JsonResponse({"exchange_data": all_data2})
                
        except Exception as e:
            print("Exchange fetch error:", e) 
            return JsonResponse({"error": "Invalid request"}, status=400)
        
    return render(request, 'exchange.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, "exchange_data": all_data})


@csrf_exempt
def sales(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    user_email = data.get('email')

    users_id_doc = DB.users.find_one({'email': user_email})

    print("✅ Sales page started")

    def generate_secure_invoice_id(length=10):
        alphabet = string.ascii_uppercase + string.digits
        return 'INV-' + localtime(timezone.now()).strftime("%Y") + ''.join(secrets.choice(alphabet) for _ in range(length))

    if request.method == "POST":
        try: 
            data = json.loads(request.body)
            scanned_data = data.get("data", {})
            print(scanned_data)

            while True:
                invoice_id = generate_secure_invoice_id()
                if not DB.products_sold.find_one({"invoice_id": invoice_id}):
                    break

            products_list = []
            product_sold = {}
            for qr_id in scanned_data["qr_ids"]:
                product_sold_data = DB.product_sold.find_one({"qrcode_ids": qr_id})
                if not product_sold_data:
                    product = DB.products.find_one({"qrcode_ids": qr_id})
                    product_id = str(product["_id"])

                    if product:

                        exists = any(p["product_id"] == product_id for p in products_list)

                        if exists:
                            for p in products_list:
                                if p["product_id"] == product_id:
                                    p["sets_sold"] += 1
                                    p["total_selling_price"] = p["price_per_item"] * p["sets_size"] * p["sets_sold"]

                        else:

                            saved_image_urls = []
                            quantity = 0

                            for i in range(len(product['variants'])):
                                image_result_url = product['variants'][i]['result_image']
                                saved_image_urls.append(image_result_url)

                            try:
                                selling_price_per_item = int(product.get("product_selling_price", 0))
                                buy_price_per_item = int(product.get("product_bought_price", 0))
                            except ValueError:
                                selling_price_per_item = 0
                                buy_price_per_item = 0

                            variants = product.get("variants", [])
                            quantity = len(variants)
                            total_selling_price = selling_price_per_item * quantity

                            product_entry = {
                                "qrcode_ids": qr_id,
                                "product_id": product_id,
                                "product_name": product.get("product_name", "N/A"),
                                "sets_sold": 1,
                                "sets_size": quantity,
                                "price_per_item": selling_price_per_item,
                                "item_buyed_price": buy_price_per_item,
                                "total_selling_price": total_selling_price,
                                "product_result_images": saved_image_urls
                            }

                            products_list.append(product_entry)

                        DB.products.update_one(
                            {"qrcode_ids": qr_id},
                            {
                                "$inc": {"sets_available": -1},
                                "$pull": {"qrcode_ids": qr_id}
                            }
                        )
                    else:
                        return JsonResponse({"error": "Product Not Found"}, status=400)
                    
                else:
                    return JsonResponse({"error": "Product already sold."}, status=400)
                
            product_sold = {
                "user_id": str(users_id_doc['_id']),
                "invoice_id": invoice_id,
                "total_amount": scanned_data['total_bill'],
                'original_amount': scanned_data['original_amount'],
                'discounted_amount': scanned_data['discounted_amount'],
                'discount_percentage': scanned_data['discount_percentage'],
                'customer_given_amount': scanned_data['customer_amount'],
                'less': scanned_data['amount_less_more'],
                "customer_phone": scanned_data['phone'],
                "customer_name": scanned_data['customer_name'],
                "sold_on": localtime(timezone.now()),
                "products": products_list
            }
            
            DB.products_sold.insert_one(product_sold)
            
            send_invoice_whatsapp_message(
                recipient_number=scanned_data['phone'],
                user_name=scanned_data['customer_name'],
                company_name=users_id_doc['shop_name'],
                amount=scanned_data['total_bill'],
                invoice_id=invoice_id,
            )


            return JsonResponse({'uploaded_urls': "uploaded"})
                
        except Exception as e:
            print("Sales fetch error:", e) 
            return JsonResponse({"error": "Invalid request"}, status=400)

    return render(request, 'sales.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})


@csrf_exempt
def search_whatsapp_number(request):
    if request.method == "POST":
        data = json.loads(request.body)
        phone = data.get("phone")

        record = DB.customers.find_one({"phone": phone})

        if record:
            record_purchases = list(DB.products_sold.find({"customer_phone": phone}))
            if record_purchases:
                purchases = []
                total_products_sold = 0 

                for sale in record_purchases:
                    products = sale.get("products", [])

                    if products:
                        total_products_sold += products[0].get("sets_sold", 0)

                        product_name = products[0].get("product_name") if products else "Unnamed Product"
                        product_quantity = total_products_sold
                        product_selling_price = products[0].get("total_selling_price") if products else 0
                        
                        purchases.append({
                            "product": product_name,
                            "qty": product_quantity,
                            "price": product_selling_price
                        })

                return JsonResponse({
                    "found": True,
                    "name": record['name'],
                    "phone": record['phone'],
                    "purchases": purchases
                })
            
            # No purchases case
            return JsonResponse({
                "found": True,
                "name": record.get("name", ""),
                "phone": record.get("phone", ""),
                "no_purchases": True
            })
        
        return JsonResponse({"found": False})
    
    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def add_whatsapp_number(request):
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        phone = data.get("phone")

        # Add to DB
        record = {
            'name': name,
            'phone': phone,
            'created': localtime(timezone.now()).strftime("%d-%m-%Y")
        }
        DB.customers.insert_one(record)

        return JsonResponse({"message": "Number added successfully"})
    
    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def get_product_by_qrcode(request):
    if request.method == "POST":
        body = json.loads(request.body)
        qr_id = body.get("qr_id")

        if not qr_id:
            return JsonResponse({"error": "No QR ID provided."}, status=400)

        # Search where qr_id is in the array field qrcode_ids
        product = DB.products.find_one({"qrcode_ids": qr_id})

        if product:
            product["_id"] = str(product["_id"])
            return JsonResponse({'data': product})

        return JsonResponse({"error": "Product not found."}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@csrf_exempt
def get_product_sold_by_qrcode(request):
    if request.method == "POST":
        body = json.loads(request.body)
        qr_id = body.get("qr_id")

        if not qr_id:
            return JsonResponse({"error": "No QR ID provided."}, status=400)

        # Search where qr_id is in the array field qrcode_ids
        product = DB.product.find_one({"qrcode_ids": qr_id})

        if product:
            product["_id"] = str(product["_id"])
            return JsonResponse({'data': product})

        return JsonResponse({"error": "Product not found."}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def get_time_range(period):
    now = localtime(timezone.now())
    if period == "Last 24 hour":
        return now - timedelta(hours=24)
    elif period == "Last week":
        return now - timedelta(days=7)
    elif period == "Last month":
        return now - timedelta(days=30)
    elif period == "Last year":
        return now - timedelta(days=365)
    return now - timedelta(days=7)  # default


@csrf_exempt
def analytics(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    user_email = data.get('email')
    user_record = DB.users.find_one({"email": user_email})
    user_id = str(user_record['_id'])

    def parse_timezone(sold_on):
        try:
            if isinstance(sold_on, dict) and "$date" in sold_on:
                val = sold_on["$date"]
                if isinstance(val, (int, float)):
                    dt = datetime.fromtimestamp(val / 1000.0, tz=dt_timezone.utc)
                elif isinstance(val, str):
                    dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
                else:
                    return localtime(timezone.now())
            elif isinstance(sold_on, (int, float)):
                dt = datetime.fromtimestamp(sold_on / 1000.0, tz=dt_timezone.utc)
            elif isinstance(sold_on, str):
                dt = datetime.fromisoformat(sold_on.replace("Z", "+00:00"))
            elif isinstance(sold_on, datetime):
                if sold_on.tzinfo is None:
                    dt = make_aware(sold_on)
                else:
                    dt = sold_on
            else:
                return localtime(timezone.now())

            return localtime(dt)  # ✅ Convert to Asia/Kolkata using Django settings
        except Exception as e:
            print("timezone parse error:", e)
            return localtime(timezone.now())


    if request.method == "POST":
        body = json.loads(request.body)
        period = body.get('range', 'Last 24 hour')

        from_date = get_time_range(period)
        # from_date = localtime(timezone.now()) - timedelta(days=7)  # includes last 7 days
        now = localtime(timezone.now())

        all_sales = list(DB.products_sold.find({
            "user_id": user_id,
        }))

        # Filter sales in the given period (local/azure-safe)
        sales = []
        for s in all_sales:
            sold_timezone = parse_timezone(s.get("sold_on"))
            if from_date <= sold_timezone < now:
                s["_sold_timezone"] = sold_timezone
                sales.append(s)

        # --- Stats ---
        total_profit = sum(
            ((p.get("price_per_item", 0) - p.get("item_buyed_price", 0)) * (p.get("sets_size", 0) * p.get("sets_sold", 0)))
            for s in sales for p in s.get("products", [])
        )

        total_customers = len(set(s.get("customer_phone") for s in sales if s.get("customer_phone")))
        total_transactions = len(sales)
        total_products = sum(
            sum(p.get("sets_sold", 0) for p in s.get("products", []))
            for s in sales
        )


        # --- Revenue Chart ---
        hourly = {}
        for s in sales:
            dt = s["_sold_timezone"]
            hour_label = dt.strftime("%d-%m %H:00")
            hourly.setdefault(hour_label, 0)
            hourly[hour_label] += float(s.get("total_amount") or 0)

        revenue_chart = [
            {"name": hour, "revenue": revenue}
            for hour, revenue in sorted(hourly.items())
        ]

        # --- Top Products ---
        product_counter = Counter()
        product_info = {}

        for s in sales:
            for p in s.get("products", []):
                pid = str(p.get("product_id"))
                product_counter[pid] += p.get("sets_sold", 0)
                
                if pid not in product_info:
                    product_info[pid] = {
                        "name": p.get("product_name", ""),
                        "image": p.get("product_result_images", [""])[0]
                    }

        top_products = []
        for pid, count in product_counter.most_common(5):
            info = product_info[pid]
            top_products.append({
                "name": info["name"],
                "image": info["image"],
                "sales": count
            })


        # --- Top Transactions ---
        top_sales = sorted(sales, key=lambda x: x.get("total_amount", 0), reverse=True)[:5]

        top_transactions = []
        for s in top_sales:
            sold_date = s["_sold_timezone"].strftime("%d-%m-%Y")

            # Safely get first product name from the products array
            products = s.get("products", [])
            product_name = products[0].get("product_name", "Unknown") if products else "Unknown"

            top_transactions.append({
                "customer": {
                    "id": s.get("customer_phone", "N/A"),
                    "name": s.get("customer_name", "Unknown")
                },
                "item": product_name,
                "date": sold_date,
                "purchase": s.get("total_amount", 0),
                "status": "completed"
            })


        return JsonResponse({
            "stats": {
                "revenue": {"value": total_profit, "change": 10},
                "customers": {"value": total_customers, "change": 12},
                "transactions": {"value": total_transactions, "change": 5},
                "products": {"value": total_products, "change": 3}
            },
            "revenue_chart": revenue_chart,
            "instagram": {
                "profileVisits": 120,
                "videoViews": 300,
                "postLikes": 180,
                "followersGained": 12
            },
            "top_products": top_products,
            "top_transactions": top_transactions
        }, safe=False)

    return render(request, 'analytics.html', {
        'dashboard': dashboard,
        'user_type': user_type,
        'first_name': user_name
    })


def dashboard(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'

    # === User Info ===
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    user_email = data.get('email')
    user_record = DB.users.find_one({"email": user_email})

    if not user_record:
        logger.error(f"User record not found for email: {user_email}. Redirecting to login.")
        return JsonResponse({'error': 'User not found. Please log in again.'}, status=404)
        
    user_id = str(user_record['_id'])

    # encryption_salt = request.session.get('encryptionSalt', user_email)
    # aes_key_bytes = derive_aes_key(user_record['password'], encryption_salt)

    try:
        recent_activities = []

        def time_diff_string(timestamp):
            now = localtime(timezone.now())
            diff = now - timestamp
            if diff.days >= 1:
                return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
            elif diff.seconds >= 3600:
                return f"{diff.seconds // 3600} hour(s) ago"
            elif diff.seconds >= 60:
                return f"{diff.seconds // 60} min ago"
            return "just now"

        def parse_timezone(sold_on):
            try:
                if isinstance(sold_on, dict) and "$date" in sold_on:
                    val = sold_on["$date"]
                    dt = datetime.fromtimestamp(val / 1000.0, tz=dt_timezone.utc)
                elif isinstance(sold_on, (int, float)):
                    dt = datetime.fromtimestamp(sold_on / 1000.0, tz=dt_timezone.utc)
                elif isinstance(sold_on, str):
                    dt = datetime.fromisoformat(sold_on.replace("Z", "+00:00"))
                elif isinstance(sold_on, datetime):
                    dt = sold_on if sold_on.tzinfo else make_aware(sold_on)
                else:
                    return localtime(timezone.now())
                return localtime(dt)
            except Exception as e:
                print("parse_timezone error:", e)
                return localtime(timezone.now())

        # === Revenue Calculation ===
        now = localtime(timezone.now())
        start_of_year = make_aware(datetime(now.year, 1, 1))
        start_ts = int(start_of_year.timestamp() * 1000)
        now_ts = int(now.timestamp() * 1000)

        revenue_pipeline = [
            {
                "$match": {
                    "user_id": user_id,
                    "sold_on": {"$gte": start_ts, "$lte": now_ts}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_revenue": {"$sum": "$total_amount"}
                }
            }
        ]

        revenue_result = list(DB.products_sold.aggregate(revenue_pipeline))
        total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0

        # === Recent Activities (no sorting in DB) ===
        sales_logs = list(DB.products_sold.find({"user_id": user_id}))
        for sale in sales_logs:
            sold_time = parse_timezone(sale.get("sold_on"))
            sale["_sold_on_dt"] = sold_time

        # Sort in Python
        sorted_sales = sorted(sales_logs, key=lambda x: x["_sold_on_dt"], reverse=True)[:5]

        for sale in sorted_sales:
            product_name = sale.get("products", [{}])[0].get("product_name", "Unnamed Product")

            recent_activities.append({
                "type": "sold",
                "product_name": product_name,
                "time": time_diff_string(sale["_sold_on_dt"])
            })

        # === Image Count ===
        image_docs = list(DB.images_download.find({
            "user_id": user_id,
            "is_downloaded": False
        }))
        image_count = sum(len(doc.get("image_urls", [])) for doc in image_docs)

        # === Video Count ===
        video_count = DB.videos_download.count_documents({
            "user_id": user_id,
            "is_downloaded": False,
            "video_urls": {"$nin": ["", " "]}
        })

        # === Top Selling Products ===
        pipeline = [
            { "$match": { "user_id": user_id }},
            { "$unwind": "$products" },
            {
                "$group": {
                    "_id": "$products.product_id",
                    "total_sets_sold": { "$sum": "$products.sets_sold" },
                    "total_items_sold": {
                        "$sum": {
                            "$multiply": ["$products.sets_sold", "$products.sets_size"]
                        }
                    },
                    "average_price": { "$avg": "$products.total_selling_price" },
                    "product_name": { "$first": "$products.product_name" },
                    "image": {
                        "$first": {
                            "$arrayElemAt": ["$products.product_result_images", 0]
                        }
                    }
                }
            },
            { "$sort": SON([("total_sets_sold", -1)]) },
            { "$limit": 5 }
        ]



        top_selling = list(DB.products_sold.aggregate(pipeline))
        for product in top_selling:
            product["product_name"] = product.get("product_name", "")
            product["image"] = product.get("image", "")

        # === Render Page ===
        if user_type == 'Employee':
            return render(request, 'barcode.html', {
                'dashboard': dashboard,
                'user_type': user_type,
                'first_name': user_name
            })

        return render(request, 'dashboard.html', {
            'dashboard': dashboard,
            'user_type': user_type,
            'first_name': user_name,
            'image_count': image_count,
            'video_count': video_count,
            'top_selling_products': top_selling,
            'total_revenue': total_revenue,
            'recent_activities': recent_activities
        })

    except Exception as e:
        print("Dashboard Error:", str(e))
        return render(request, 'analytics.html', {
            'error_message': str(e)
        })
    


def download_product_image(request):
    url = request.GET.get('url')
    if not url:
        return HttpResponse("No URL provided", status=400)

    r = requests.get(url, stream=True)
    filename = url.split("/")[-1]
    
    response = HttpResponse(r.content, content_type=r.headers['Content-Type'])
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response



def download_images_zip(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'

    # === User Info ===
    user_email = data.get('email')
    user_record = DB.users.find_one({"email": user_email})
    user_id = str(user_record['_id'])

    # 1. Fetch all image documents that are not downloaded
    image_docs = list(DB.images_download.find({
        "user_id": user_id,
        "is_downloaded": False
    }))

    # 2. Prepare a zip in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for idx, doc in enumerate(image_docs):
            image_urls = doc.get("image_urls", [])
            for i, url in enumerate(image_urls):
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        ext = url.split(".")[-1].split("?")[0]  # remove query string
                        filename = f"image_{idx+1}_{i+1}.{ext}"
                        zip_file.writestr(filename, response.content)
                except Exception as e:
                    print(f"Error downloading {url}: {e}")

    # 3. Mark all as downloaded
    DB.images_download.update_many({"is_downloaded": False}, {"$set": {"is_downloaded": True}})

    # 4. Return the zip as an HTTP response
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="images_download.zip"'
    return response


def download_videos_zip(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'

    # === User Info ===
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    user_email = data.get('email')
    user_record = DB.users.find_one({"email": user_email})
    user_id = str(user_record['_id'])

    # 1. Fetch all video documents not yet downloaded with valid URLs
    video_docs = list(DB.videos_download.find({
        "user_id": user_id,
        "is_downloaded": False,
        "video_urls": {
            "$regex": r"^https://fitattirestorage\.blob\.core\.windows\.net/fitattire-assets/",
            "$options": "i"
        }
    }))

    # 2. Prepare a zip file in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for idx, doc in enumerate(video_docs):
            video_url = doc.get("video_url")
            if not video_url:
                continue
            try:
                response = requests.get(video_url, stream=True)
                if response.status_code == 200:
                    ext = video_url.split(".")[-1].split("?")[0]
                    filename = f"video_{idx+1}.{ext}"
                    zip_file.writestr(filename, response.content)
                else:
                    print(f"Failed to fetch {video_url}: Status {response.status_code}")
            except Exception as e:
                print(f"Error downloading {video_url}: {e}")

    # 3. Mark only these docs as downloaded
    video_ids = [doc['_id'] for doc in video_docs]
    if video_ids:
        DB.videos_download.update_many(
            {"_id": {"$in": video_ids}},
            {"$set": {"is_downloaded": True}}
        )

    # 4. Send zip file as response
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="videos_download.zip"'
    return response



def product_list(request, shop_name, user_id):
    try:
        user = DB.users.find_one({"_id": user_id})
        if not user:
            return render(request, "404.html", {"message": "User not found"})

        shop_name1 = user.get('shop_name', '')

        products = list(DB.products.find({"user_id": user_id}))

        # products = []

        # for p in products_cursor:
        #     variants = p.get("variants", [])
        #     if variants:
        #         first_variant = variants[0]
        #         first_image = first_variant.get("result_image") or first_variant.get("garment_image", "")

        #         products.append({
        #             "product_name": p.get("product_name", ""),
        #             "gender": p.get("product_gender", ""),
        #             "age_group": p.get("age_group", "Adults"),
        #             "category": p.get("product_category", ""),
        #             "subcategory": p.get("product_subCategory", ""),
        #             "final_category": p.get("product_finalCategory", ""),
        #             "selling_price": p.get("product_selling_price", ""),
        #             "color": first_variant.get("color", ""),
        #             "image": first_image,
        #             "barcode": p.get("qrcode_ids", [""])[0].rstrip("/"),
        #         })

        return render(request, "product_list.html", {
            "products": products,
            "business_name": shop_name1
        })
    
    except Exception as e:
        return render(request, "500.html", {"message": f"Server error: {str(e)}"})


def contact_us(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    
    return render(request, 'contact_us.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})



@csrf_exempt
def barcode(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    

    num = '0'
    sum1 = 0
    product_name_list = [] 
    global product_list1

    if request.method == 'POST':
        try:
            if request.POST.get("form_type") == 'rm_data1':
                barcodeInput = request.POST.get("barcodeInput1")
                number = '1'

                barcode_doc = DB.products.find_one({"barcode": barcodeInput})

                new_quantity = int(barcode_doc['left_quantity']) - 1

                DB.products.find_one_and_update({'barcode': barcodeInput}, {'$set': {'left_quantity': new_quantity}})

                if barcode_doc:
            
                    product_list1.append(barcode_doc)
                    for data in product_list1:

                        sum1 = sum1 + int(data['selling_price'])

                    return render(request, 'barcode.html', { 'dashboard': 
			    									   dashboard, 'user_type': user_type, 'first_name': user_name, 'barcode_data': product_list1, 'barcode_doc': barcode_doc, 'num': number, 'totalMoney' : sum1})
                else:
                    raise Exception


            elif request.POST.get("form_type") == 'delete_data':
                deleted_product_barcode = request.POST.get("deleted_product")
                number = '1'

                barcode_doc = DB.products.find_one({"barcode": deleted_product_barcode})
                barcode_doc['left_quantity'] = int(barcode_doc['left_quantity']) + 1

                for i in range(len(product_list1)):
                    if product_list1[i]['barcode'] == deleted_product_barcode:
                        del product_list1[i]
                        break

                for data in product_list1:

                        sum1 = sum1 + int(data['selling_price'])

                return render(request, 'barcode.html', { 'dashboard': 
			    									   dashboard, 'user_type': user_type, 'first_name': user_name, 'barcode_data': product_list1, 'barcode_doc': barcode_doc, 'num': number, 'totalMoney' : sum1})


            elif request.POST.get("form_type") == 'rm_data2':
                number1 = '2'

                for data in product_list1:

                    product_name_list.append(data['product_name']) 

                    sum1 = sum1 + int(data['selling_price'])

                    products_dict = {
	                    "product_name": data['product_name'],
	                    "cost_price": data['cost_price'],
	                    "selling_price": data['selling_price'],
	                    "expiry_date": data['expiry_date'],
	                    "profit": data['profit'],
	                    "barcode": data['barcode'],
	                    "image": data['image'],
	                    "date_time": localtime(timezone.now()),
                        "user_id": data['user_id'],
	                }
                    DB.products_sold.insert_one(products_dict)

                a = len(product_list1)

                return render(request, 'barcode.html', { 'dashboard': 
			    									   dashboard, 'user_type': user_type, 'first_name': user_name, 'barcode_product_name': product_name_list, 'num': number1, 'scanned_quantity': a, 'scanned_quantity_totalPrice': sum1})
            
            else:
                raise Exception
            
        except:
            messages.warning(request, "Outside Product")
            num = '0'
            return render(request, 'barcode.html',  { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'num': num})
            
    else:
        product_list1 = []
        return render(request, 'barcode.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'num': num})



def employee(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    user_email = data.get('email')

    users_id_doc = DB.users.find_one({'email': user_email})

    employees_doc = list(DB.employees.find({'user_id': users_id_doc['_id']}))

    if request.method == 'POST':
        print("1")
        employee_email = request.POST.get("email")
        employee_firstname = request.POST.get("first_name")
        employee_lastname = request.POST.get("last_name")
        employee_mobile = request.POST.get("mobile")
        employee_age = request.POST.get("age")
        employee_address = request.POST.get("address")
        employee_salary = request.POST.get("salary")

        DB.employees.find_one_and_update(
            {"email": employee_email}, {'$set': 
                {
                'first_name': employee_firstname,
                'last_name': employee_lastname,
                'mobile': employee_mobile,
                'age': employee_age,
                'address': employee_address,
                'salary': employee_salary,
                }
            }
        )
        print("2")
        employees_doc1 = list(DB.employees.find({'user_id': users_id_doc['_id']}))
        print("3")

        return render(request, 'employee.html', { 'dashboard': 
												   dashboard, 'user_type': user_type, 'first_name': user_name, 'employees_doc': employees_doc1, 'show': '0'}) 
            
    else:
        return render(request, 'employee.html', { 'dashboard': 
													dashboard, 'user_type': user_type, 'first_name': user_name, 'employees_doc': employees_doc, 'show': '0'})



@csrf_exempt
def employee_signup(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_email = data.get('email')
    user_name = data.get('first_name')
    
    
    if request.method == 'POST':
        try:
            employee_email = request.POST.get("email")
            employee_doc = DB.users.find_one({"email": employee_email})

            if not employee_doc:

                employee_firstname = request.POST.get("first_name")
                employee_lastname = request.POST.get("last_name")
                employee_mobile = request.POST.get("mobile")
                employee_age = request.POST.get("age")
                employee_address = request.POST.get("address")
                employee_salary = request.POST.get("salary")

                employee_password = request.POST.get("password")


                user_doc = DB.users.find_one({"email": user_email})
                user_id = user_doc['_id']

                employee_dict = {
	                "first_name": employee_firstname,
	                "last_name": employee_lastname,
	                "mobile": employee_mobile,
	                "age": employee_age,
	                "address": employee_address,
	                "salary": employee_salary,
	                "email": employee_email,
	                "password": generate_password(employee_password),
	                "user_type": 'Employee',
                    "user_id": user_id,
	            }
                user_dict = {
                    "login_type": "username-pass",
	                "first_name": employee_firstname,
	                "last_name": employee_lastname,
	                "email": employee_email,
	                "password": generate_password(employee_password),
	                "user_type": 'Employee',
	            }

                DB.employees.insert_one(employee_dict)
                DB.users.insert_one(user_dict)
                employees_doc = list(DB.employees.find({'user_id': user_id}))
                return render(request, 'employee.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'employees_doc': employees_doc, 'show': '0'})

            else:
                raise Exception
            
        except:
            messages.warning(request, "Already Registered")
            return render(request, 'employee_signup.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})
            
    else:
        return render(request, 'employee_signup.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})






def shops(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    shops_details = list(DB.shops.find({"user_type": "Shops"}))
    
    return render(request, 'shops.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'shops_details': shops_details})




def shops_add(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    
    if request.method == 'POST':
        try:
            shop_contact = request.POST.get("shop_contact")
            shops_doc = DB.shops.find_one({"shop_contact_number": shop_contact})

            if not shops_doc:

                shop_name = request.POST.get("shop_name")
                shop_address = request.POST.get("shop_address")
                shop_contact = request.POST.get("shop_contact")
       
                shops_dict = {
	                "shop_name": shop_name,
	                "shop_address": shop_address,
	                "shop_contact_number": shop_contact,
	                "user_type": 'Shops',
	            }

                DB.shops.insert_one(shops_dict)

                return redirect("/shops/")

            else:
                raise Exception
            
        except:
            messages.warning(request, "Already Registered")
            return render(request, 'shops_add.html')
            
    else:
        return render(request, 'shops_add.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})




def users_details(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    shop_owners_details = list(DB.users.find({'user_type': 'Shop Owners'}))

    
    return render(request, 'users_details.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'shop_owners_details': shop_owners_details})


def users_products(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    # shop_owners_details = list(DB.users.find({'user_type': 'Shop Owners'}))
    shop_owners_details = list(DB.users.find({
        'user_type': { '$in': ['Shop Owners', 'Shop_Owners_2'] }
    }))

    for shop in shop_owners_details:
        shop['id'] = str(shop['_id'])  # rename
        del shop['_id']  # optional: remove the original

    
    return render(request, 'users_products.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'shop_owners_details': shop_owners_details})


def shop_products_details(request, shop_id):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    shop = list(DB.products_2.find({'user_id': shop_id}))

    return render(request, 'shop_products_details.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'shop_product_details': shop})

    

@csrf_exempt
def users_signup(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    if request.method == 'POST':
        try:
            users_email = request.POST.get("Email")
            users_email_lower = users_email.lower() 
            users_doc = DB.users.find_one({"email": users_email_lower}) 

            if not users_doc:
                users_firstname = request.POST.get("FirstName")
                users_lastname = request.POST.get("LastName")
                users_shop_name = request.POST.get("ShopName")
                users_shop_address = request.POST.get("ShopAddress")
                users_shop_logo = request.FILES.get('LogoImage')
                users_garments_type = request.POST.get("shop_type")
                users_phone_number = request.POST.get("PhoneNumber")
                instagram_link = request.POST.get("instagram_url")
                # users_status_value = request.POST.get("StatusValue")
                users_password = request.POST.get("Password")

                shop_logo_url = None
                if users_shop_logo:
                    shop_logo_url = upload_image_to_azure(users_shop_logo, blob_name="shop_logo")

                encryption_pbkdf2_salt = os.urandom(16).hex()

                users_dict = {
	                "first_name": users_firstname,
	                "last_name": users_lastname,
	                "mobile": users_phone_number,
	                # "status": users_status_value,
	                "garments_type": users_garments_type,
	                "shop_name": users_shop_name,
	                "shop_address": users_shop_address,
	                "shop_logo": shop_logo_url,
	                "email": users_email_lower,
	                "instagram_url": instagram_link,
                    "plan_type": "Plus Plan",
                    "credits_given": 100,
                    "credits_used": 0,
	                "password": generate_password(users_password),
	                "user_type": 'Shop Owners',
                    "encryption_pbkdf2_salt": encryption_pbkdf2_salt,
	            }
                DB.users.insert_one(users_dict)
                logger.info(f"New user {users_email_lower} registered successfully.")

                shop_owners_details = list(DB.users.find({'user_type': 'Shop Owners'}))
                return render(request, 'users_details.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'shop_owners_details': shop_owners_details})

            else:
                raise Exception
            
        except:
            messages.warning(request, "Already Registered")
            return render(request, 'users_signup.html')
            
    else:
        return render(request, 'users_signup.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})



@csrf_exempt
def delete_product(request, product_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE requests allowed'}, status=405)

    try:
        # Ensure valid ObjectId
        obj_id = ObjectId(product_id)
    except Exception:
        return JsonResponse({'error': 'Invalid product ID'}, status=400)

    result = DB.products.delete_one({'_id': obj_id})
    
    if result.deleted_count == 1:
        return JsonResponse({'message': 'Product deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Product not found'}, status=404)


@csrf_exempt
def delete_product_2(request, product_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE requests allowed'}, status=405)

    try:
        # Ensure valid ObjectId
        obj_id = ObjectId(product_id)
    except Exception:
        return JsonResponse({'error': 'Invalid product ID'}, status=400)

    result = DB.products_2.delete_one({'_id': obj_id})
    
    if result.deleted_count == 1:
        return JsonResponse({'message': 'Product deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Product not found'}, status=404)


def delete(request):
    try:
        a = request.GET.get('q', '')
        if '@' in a:
            DB.employees.delete_one({'email': a})
            DB.users.delete_one({'email': a})
            return redirect("/employee/")
        else:
            DB.shops.delete_one({'shop_contact_number': a})
            return redirect("/shops/")
    except:
        return redirect("/shops/")
    


def detail(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    try:
        a = request.GET.get('q', '')
        employee_detail = DB.employees.find_one({'email': a})
        return render(request, 'employee.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'employee_detail': employee_detail, 'show': '1'})
    except:
        return redirect("/employee/")
    

    
def update(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
    user_email = data.get('email')

    users_id_doc = DB.users.find_one({'email': user_email})

    if request.method == 'POST':
        employee_email = request.POST.get("email")
        employee_firstname = request.POST.get("first_name")
        employee_lastname = request.POST.get("last_name")
        employee_mobile = request.POST.get("mobile")
        employee_age = request.POST.get("age")
        employee_address = request.POST.get("address")
        employee_salary = request.POST.get("salary")

        DB.employees.find_one_and_update(
            {"email": employee_email}, {'$set': 
                {
                'first_name': employee_firstname,
                'last_name': employee_lastname,
                'mobile': employee_mobile,
                'age': employee_age,
                'address': employee_address,
                'salary': employee_salary,
                }
            }
        )
        employees_doc1 = list(DB.employees.find({'user_id': users_id_doc['_id']}))

        return render(request, 'employee.html', { 'dashboard': 
												   dashboard, 'user_type': user_type, 'first_name': user_name, 'employees_doc': employees_doc1, 'show': '0'}) 
    else:
        try:
            a = request.GET.get('q', '')
            employee_detail = DB.employees.find_one({'email': a})
            return render(request, 'employee.html', { 'dashboard': 
	    												   dashboard, 'user_type': user_type, 'first_name': user_name, 'employee_detail': employee_detail, 'show': '2'})
        except:
            return redirect("/employee/")


@csrf_exempt
def login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get("email")
            login_password = request.POST.get("password")

            user_doc = DB.users.find_one({"email": email})
            if user_doc:
                userBytes = login_password.encode('utf-8')
                doc_pass = user_doc['password']
                result = bcrypt.checkpw(userBytes, doc_pass)

                if result:
                    # ✅ Prepare JWT payload
                    email = user_doc.get("email")
                    user_type = user_doc.get("user_type")
                    first_name = user_doc.get("first_name")
                    user_dict = {
                        "email": email,
                        "user_type": user_type,
                        "first_name": first_name,
                    }

                    # ✅ Store JWT token
                    jwt_token = generate_token(user_dict)
                    response = HttpResponseRedirect('/dashboard')
                    
                    response.set_cookie(
                        "t",
                        jwt_token,
                        httponly=True,        # Prevent JS access
                        secure=True,          # Only send over HTTPS
                        samesite="Lax",       # Safe default
                        max_age=60*60*12      # 12 hours in seconds
                    )

                    DB.users.find_one_and_update({"email": email}, {"$set": {"token": jwt_token}})

                    # request.session['encryptionPassword'] = login_password
                    # request.session['encryptionSalt'] = email  

                    return response
                else:
                    raise Exception
            else:
                raise Exception

        return render(request, 'login.html', {})
    except:
        messages.warning(request, "Invalid ID or Password")
        logger.error("Failed system of logging in.")
        return render(request, 'login.html')


def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie("t")
    return response


@csrf_exempt 
def get_user_encryption_salt(request):
    """
    Retrieves the unique PBKDF2 encryption salt for a given user's email.
    This salt is used client-side for deriving the encryption key.
    """
    if request.method == 'GET':
        email = request.GET.get('email')
        if not email:
            logger.warning("Attempt to get encryption salt without providing email.")
            return JsonResponse({'error': 'Email is required'}, status=400)
        
        print("15.3")

        # Fetch only the 'encryption_pbkdf2_salt' field for the given email
        # This prevents leaking other user details.
        user_doc = DB.users.find_one({"email": email}, {"encryption_pbkdf2_salt": 1}) 

        if user_doc and user_doc.get('encryption_pbkdf2_salt'):
            print("15.4")
            logger.info(f"Successfully retrieved encryption salt for email: {email}")
            return JsonResponse({'encryption_salt': user_doc['encryption_pbkdf2_salt']})
        else:
            # Important: Return a generic "not found" or "invalid user" error
            # to prevent email enumeration (i.e., don't tell an attacker if an email exists or not).
            logger.warning(f"Encryption salt not found for email: {email} or user does not exist.")
            print("15.5")
            return JsonResponse({'error': 'Invalid user or salt not available.'}, status=404)
    else:
        logger.warning(f"Invalid request method for get_user_encryption_salt: {request.method}")
        return JsonResponse({'error': 'Invalid request method. Only GET is allowed.'}, status=405)
