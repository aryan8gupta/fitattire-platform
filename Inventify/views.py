from django.conf import settings
from bson import ObjectId
from bson.son import SON
from django.contrib import messages;
from django.shortcuts import render, redirect;
from django.http import HttpResponseRedirect, HttpResponse

import bcrypt 
import jwt
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
# from Inventify.settings import DB, JWT_SECRET_KEY, MEDIA_ROOT
from Inventify.deployment import DB, JWT_SECRET_KEY, MEDIA_ROOT
from .models import YourModel
from video_generator.generate_text_photos import create_dynamic_photo_with_auto_closeup, create_offer_photo_with_right_image 
from video_generator.instagram_post_test import post_to_instagram, post_azure_video_to_instagram
from video_generator.generate_video import start_video_generation
from video_generator.send_whatsapp import send_invoice_whatsapp_message

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
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .utils.blob_utils import upload_image_to_azure

from openai import OpenAI
import secrets

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


my_var_2 = os.getenv('Open_API_Key', 'Default Value')
client = OpenAI(api_key=my_var_2)

my_var_1 = os.getenv('New_Pincel_API_Key', 'Default Value')

PINCEL_API_URL = "https://pincel.app/api/clothes-swap"
PINCEL_API_KEY = my_var_1

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
TOP_MARGIN_MM = 10
LEFT_MARGIN_MM = 10
GAP_X_MM = 5   # Horizontal gap
GAP_Y_MM = 0   # ✅ MINIMAL vertical gap to fit 8 rows

def mm_to_pt(mm_val):
    return mm_val * mm

def generate_qr_code(data, filename):
    qr = qrcode.make(data)
    qr.save(filename)
    return filename

def create_qr_label_pdf(start_id=10000, total_labels=240, output_file="qr_labels.pdf"):
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



# create_qr_label_pdf(start_id=10001, total_labels=240)

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
    token = jwt.encode({"exp": datetime.now() + timedelta(days=7) , **user_dict}, JWT_SECRET_KEY, algorithm="HS256")
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
        if result:
            random_integer = random.randint(100, 300)
            upgraded_product_price = int(result['selling_price']) + random_integer
            product_discount = int(((random_integer)/(upgraded_product_price)) * 100)
            return render(request, 'product_display.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, 'product': result, 'discount': product_discount, 'product_price': upgraded_product_price, "show_edit": valid, 'product_id': result['_id']})

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

        user_id = records[0].get('user_id')
        user_record = DB.users.find_one({"_id": user_id})

        users_shop_logo = user_record['shop_logo']
        users_shop_address = user_record['shop_address']
        users_shop_name = user_record['shop_name']
        users_phone = user_record['mobile']

    else:
        print("No Product Found")
        return render(request, 'invoice.html')

    return render(request, 'invoice.html',  {
        'records': records, 
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
        model_image = request.POST.get('model_image_url')
        garment_image = request.FILES.get('garment_image')

        if not model_image or not garment_image:
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

        resized_model_path = os.path.join(MEDIA_ROOT, 'resized_model_image.jpg')
        resize_image(model_image, resized_model_path)
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
                        upscale_image(data2.get('output'), upscaled_path)

                        # First Saving the Result
                        output_path = os.path.join(MEDIA_ROOT, 'api_result.jpg')
                        save_api_result_from_url(data2.get('output'), output_path)

                        try:
                            # Upload to Azure
                            upscaled_azure_url = upload_image_to_azure(upscaled_path, blob_name="result")
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
    users_id = user_record['_id']
    print(users_id)

    credits = user_record.get("credits_used", 0)

    print("✅ Add Product page started")

    if request.method == 'POST':
        try:
            print("🔍 Reading POST data...")
            logger.info("reading post data")

            # ✅ Safely get the data sent as FormData
            json_data1 = request.POST.get('document')
            json_data2 = request.POST.get('selectedmiddlebuttons')
            logger.info("reading post data-2")

            if not json_data1:
                print("❌ 'document' is missing in POST")
                return JsonResponse({'error': 'Missing product data'}, status=400)

            parsed_data1 = json.loads(json_data1)
            parsed_data2 = json.loads(json_data2)

            # Prepare to save uploaded garment images
            saved_garment_urls = []
            saved_result_urls = []
            logger.info("reading post data-3")

            # garment_images in parsed_data1 are currently placeholders (filenames or base64 strings)
            # We replace them with actual saved media URLs after saving files

            # Loop through all garment image files sent with keys 'garment_0', 'garment_1', ...
            for i in range(len(parsed_data1['product_colors'])):
                file_key1 = f'garment_{i}'
                uploaded_garment_file = request.FILES.get(file_key1)

                if uploaded_garment_file:
                    uploaded_garment_url = upload_image_to_azure(uploaded_garment_file, blob_name="garment")
                    saved_garment_urls.append(uploaded_garment_url)
       
                else:
                    # No file sent for this variant, fallback or error handling
                    saved_garment_urls.append('')  # or handle as you prefer

            logger.info("reading post data-4")

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

            logger.info("reading post data-5")

            print(saved_garment_urls)
            print(saved_result_urls)

            generated_urls=[]
            generated_images = []

            product_name = parsed_data2.get('product_name', 'Low Rise Wide Jeans')
            category = parsed_data2.get('category', 'Jeans')
            gender = parsed_data2.get('gender', 'Women')

            random_integer = random.randint(100, 300)
            upgraded_product_price = int(parsed_data1['product_selling_price']) + random_integer
            product_discount = int(((random_integer)/(upgraded_product_price)) * 100)

            logger.info("reading post data-6")
            # Build the variants array
            variants = []
            for i in range(len(parsed_data1['product_colors'])):
                variant = {
                    "color": parsed_data1['product_colors'][i],
                    "garment_image": saved_garment_urls[i],
                    "result_image": saved_result_urls[i],
                }
                variants.append(variant)
                # For Image Generation with Text
                big_image_path = saved_result_urls[i]
                garment_image_path = saved_garment_urls[i]
                logo_path = users_shop_logo
                output_path = "generated"
                texts = [
                    f"Price: ₹{parsed_data1['product_selling_price']}",
                    f"Sizes: {parsed_data1['product_sizes']}",
                    f"Fabric: {parsed_data1['product_fabric']}",
                    f"Color: {parsed_data1['product_colors'][i]}"
                ]
                image_url_2 = create_offer_photo_with_right_image(
                    big_image_path=big_image_path,
                    output_path="generated",
                    product_id=parsed_data1['qrcode_ids'][0],
                    offer_title="Mega Deal",
                    discount_text=f"{product_discount}% OFF",
                    final_line_1="DM the Product Id to",
                    final_line_2="Know more."
                )
                logger.info("reading post data-7")

                generated_urls.append(image_url_2)

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a creative Instagram marketer who writes short, catchy, and trendy captions for fashion products in India. Use emojis and hashtags where relevant. And be concise."},
                        {
                            "role": "user",
                            "content": f"""Generate an Instagram caption for the following product:
                                Product Name: {product_name}
                                Product Category: {category}
                                Product Gender: {gender}
                                Product Fabric: {parsed_data1['product_fabric']}
                                Product Price: ₹{parsed_data1['product_price']}
                                Product Selling Price: ₹{parsed_data1['product_selling_price']}
                                Product Color: {parsed_data1['product_colors'][i]}

                                Keep it short, attention-grabbing, and its an image of a product with information like Mega Deal, {product_discount}% off, to know more about the product, enter the product id in the chat given in the image and add 3–5 relevant fashion hashtags."""
                        }
                    ]
                )

                reply = response.choices[0].message.content
                logger.info("reading post data-8")

                response = post_to_instagram(image_url_2, reply)
                print(response)

                azure_generated_image_url = create_dynamic_photo_with_auto_closeup(
                    big_image_path=big_image_path,
                    logo_path=logo_path,
                    texts=texts,
                    output_path=output_path,
                    garment_image_path=garment_image_path
                )
                generated_images.append(azure_generated_image_url)
            
            logger.info("reading post data-9")

            image_dict = {
                "user_id": users_id,
                "qr_ids": parsed_data1['qrcode_ids'],
                "image_urls": generated_images,
                "is_downloaded": False,
                "created_at": datetime.now().strftime("%d-%m-%Y")
            }

            DB.images_download.insert_one(image_dict)

            logger.info("reading post data-10")
            # Video Generation by Threading Starts ---------------->
            video_url = ''
            video_record = list(DB.videos_downloaded.find(
                {"user_id": users_id, "video_generated": False}
            ))
            logger.info("reading post data-11")
            logger.info(video_record)

            if video_record:
                for record in video_record:
                    generated_urls.append(record["image_urls"])

                if len(generated_urls) >= 3:
                    video_output_path = f"output/generated_reel_{uuid.uuid4().hex}.mp4"

                    # SAFETY: Start thread and don't store the thread object
                    def background_task():
                        video_url = start_video_generation(generated_urls, video_output_path, users_shop_address, users_shop_name)
                        
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a creative Instagram marketer who writes short, catchy, and trendy captions for fashion products in India. Use emojis and hashtags where relevant. And be concise."},
                                {
                                    "role": "user",
                                    "content": f"""Generate an Instagram caption for the following product:
                                        Product Name: {product_name}
                                        Product Category: {category}
                                        Product Gender: {gender}
                                        Product Fabric: {parsed_data1['product_fabric']}
                                        Product Price: ₹{parsed_data1['product_price']}
                                        Product Selling Price: ₹{parsed_data1['product_selling_price']}
                                        Product Color: {parsed_data1['product_colors'][i]}

                                        Keep it short, attention-grabbing, and its a video of the product with different variants of the product with information like Mega Deal, {product_discount}% off, to know more about the product, enter the product id in the chat given in the image and add 3–5 relevant fashion hashtags."""
                                }
                            ]
                        )

                        reply_2 = response.choices[0].message.content
                        
                        caption = "🔥 Fresh stock just dropped! #streetwear #fashionreel"
                        result = post_azure_video_to_instagram(video_url, reply_2)
                        print(result)

                        if video_url:
                            DB.videos_download.update_one(
                                {"user_id": users_id},
                                {'$set': 
                                    {
                                        "video_urls": video_url,
                                        "video_generated": True,
                                        "image_urls": generated_urls,
                                    }
                                }
                            )
                    thread = threading.Thread(target=background_task)
                    thread.daemon = True
                    thread.start()

                    print("[INFO] Video generation thread-1 started.")

            elif len(generated_urls) >= 3:
                video_output_path = f"output/generated_reel_{uuid.uuid4().hex}.mp4"

                # ✅ SAFETY: Start thread and don't store the thread object
                def background_task():
                    video_url = start_video_generation(generated_urls, video_output_path, users_shop_address)
                        
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a creative Instagram marketer who writes short, catchy, and trendy captions for fashion products in India. Use emojis and hashtags where relevant. And be concise."},
                            {
                                "role": "user",
                                "content": f"""Generate an Instagram caption for the following product:
                                    Product Name: {product_name}
                                    Product Category: {category}
                                    Product Gender: {gender}
                                    Product Fabric: {parsed_data1['product_fabric']}
                                    Product Price: ₹{parsed_data1['product_price']}
                                    Product Selling Price: ₹{parsed_data1['product_selling_price']}
                                    Product Color: {parsed_data1['product_colors'][i]}

                                    Keep it short, attention-grabbing, and its a video of the product with different variants of the product with information like Mega Deal, {product_discount}% off, to know more about the product, enter the product id in the chat given in the image and add 3–5 relevant fashion hashtags."""
                            }
                        ]
                    )

                    reply_2 = response.choices[0].message.content
                    
                    caption = "🔥 Fresh stock just dropped! #streetwear #fashionreel"
                    result = post_azure_video_to_instagram(video_url, reply_2)
                    print(result)

                    if video_url:
                        DB.videos_download.insert_one({
                            "user_id": users_id,
                            "qr_ids": parsed_data1['qrcode_ids'],
                            "image_urls": generated_urls,
                            "video_urls": video_url,
                            "video_generated": True,
                            "is_downloaded": False,
                            "created_at": datetime.now().strftime("%d-%m-%Y")
                        })

                thread = threading.Thread(target=background_task)
                thread.daemon = True
                thread.start()

                print("[INFO] Video generation thread-2 started.")

            else:
                logger.info("reading post data-12")
                video_dict = {
                    "user_id": users_id,
                    "qr_ids": parsed_data1['qrcode_ids'],
                    "image_urls": generated_urls,
                    "video_urls": video_url,
                    "video_generated": False,
                    "is_downloaded": False,
                    "created_at": datetime.now().strftime("%d-%m-%Y")
                }

                DB.videos_download.insert_one(video_dict)
                print("[INFO] Not enough images to start video generation.")


            products_dict = {
                "qrcode_ids": parsed_data1['qrcode_ids'],
                "product_gender": parsed_data2['gender'],
                "product_category": parsed_data2['category'],
                "product_subCategory": parsed_data2['subCategory'],
                "product_finalCategory": parsed_data2['finalCategory'],
                "product_swapCategory": parsed_data2['swapCategory'],
                "brand_name": parsed_data1['brand_name'],
                "product_name": parsed_data1['product_name'],
                "product_fabric": parsed_data1['product_fabric'],
                "product_quantity": int(parsed_data1['product_quantity']),
                "sizes": parsed_data1['product_sizes'],
                "product_price": parsed_data1['product_price'],
                "selling_price": parsed_data1['product_selling_price'],
                "variants": variants
            }
            # DB.products.create_index({"qrcode_ids": 1})
            logger.info("reading post data-13")

            DB.products.insert_one(products_dict)
            print("✅ Product inserted successfully")

            return JsonResponse({'uploaded_urls': "uploaded"})

        except Exception as e:
            print("❌ Exception:", str(e))
            return JsonResponse({'error': 'Something went wrong', 'details': str(e)}, status=500)
            

    return render(request, 'add_products.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, 'credits': credits})


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
                            "date": datetime.now().strftime("%d-%m-%Y"),
                            "product_name": product.get("product_name", "N/A"),
                            "status": scanned_data.get("status"),
                        }
                        DB.exchange.insert_one(exchange_dict)

                        if (scanned_data.get("status") == "Returned"):
                            DB.products.update_one(
                                {"qrcode_ids": qr_id},
                                {"$inc": {"product_quantity": -1}}
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
        return 'INV-' + datetime.now().strftime("%Y") + ''.join(secrets.choice(alphabet) for _ in range(length))

    if request.method == "POST":
        try: 
            data = json.loads(request.body)
            scanned_data = data.get("data", {})
            print(scanned_data)

            while True:
                invoice_id = generate_secure_invoice_id()
                if not DB.products_sold.find_one({"invoice_id": invoice_id}):
                    break
            
            for qr_id in scanned_data["qr_ids"]:
                product_sold_data = DB.product_sold.find_one({"qr_ids": qr_id})
                if not product_sold_data:
                    product = DB.products.find_one({"qrcode_ids": qr_id})
                    saved_image_urls = []
                    for i in range(len(product['variants'])):
                        image_result_url = product['variants'][i]['result_image']
                        saved_image_urls.append(image_result_url)

                    if product:
                        product_sold = {
                            "qr_id": qr_id,
                            "user_id": users_id_doc['_id'],
                            "invoice_id": invoice_id,
                            "product_id": product['_id'],
                            "product_name": product.get("product_name", "N/A"),
                            "total_amount": scanned_data['total_bill'],
                            'original_amount': scanned_data['original_amount'],
                            'discounted_amount': scanned_data['discounted_amount'],
                            'discount_percentage': scanned_data['discount_percentage'],
                            'customer_given_amount': scanned_data['customer_amount'],
                            'less': scanned_data['amount_less_more'],
                            "product_result_images": saved_image_urls,
                            "customer_phone": scanned_data['phone'],
                            "customer_name": scanned_data['customer_name'],
                            "sold_on": datetime.now()
                        }
                        DB.products_sold.insert_one(product_sold)
                        DB.products.update_one(
                            {"qrcode_ids": qr_id},
                            {
                                "$inc": {"product_quantity": -1},
                                "$pull": {"qrcode_ids": qr_id}
                            }
                        )
                
                else:
                    return JsonResponse({"error": "Product already sold."}, status=400)
            
            result = send_invoice_whatsapp_message(
                recipient_number=scanned_data['phone'],
                user_name=scanned_data['customer_name'],
                company_name=users_id_doc['shop_name'],
                amount=scanned_data['total_bill'],
                invoice_id=invoice_id,
                instagram_link=users_id_doc['instagram_url'],
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
        print("100")

        record = DB.customers.find_one({"phone": phone})
        print(record)

        if record:
            record_purchases = list(DB.products_sold.find({"phone_number": phone}))
            if record_purchases:
                purchases = []
                for p in record_purchases:
                    purchases.append({
                        "product": p.get("product_name", ""),
                        "qty": p.get("buyed_quantity", 0),
                        "price": p.get("product_sold_price", 0)
                    })

                return JsonResponse({
                    "found": True,
                    "name": record.name,
                    "phone": record.phone,
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
            'created': datetime.now().strftime("%d-%m-%Y")
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
            product["_id"] = str(product["_id"])  # Make ObjectId serializable
            return JsonResponse({'data': product})

        return JsonResponse({"error": "Product not found."}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def get_time_range(period):
    now = datetime.now()
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
    user_id = user_record['_id']

    if request.method == "POST":

        data = json.loads(request.body)
        period = data.get('range', 'Last 24 hour')
        print("120")
        print(period)
        
        from_date = get_time_range(period)
        now = datetime.now()

        # Filter products_sold based on actual datetime
        sales = list(DB.products_sold.find({
            "user_id": ObjectId(user_id),
            "sold_on": { "$gte": from_date, "$lt": now }
        }))

        # --- Stats Calculation ---
        total_profit = sum(s.get("discounted_amount", 0) for s in sales)
        total_customers = len(set(s.get("customer_phone") for s in sales))
        total_transactions = len(sales)
        total_products = len(set(s.get("product_name") for s in sales))

        # Revenue chart mock (group by hour or day for now, you can optimize later)
        revenue_chart = []
        hourly = {}
        for s in sales:
            hour_label = s["sold_on"].strftime("%H:00")  # group by hour
            hourly.setdefault(hour_label, 0)
            hourly[hour_label] += s.get("discounted_amount", 0)

        for hour, revenue in sorted(hourly.items()):
            revenue_chart.append({
                "name": hour,
                "revenue": revenue,
                "ecommerce": revenue // 2  # just mock
            })

        # Example static placeholders for top_products and top_transactions
        top_products = [
            {"name": "Denim Jacket", "image": "https://cdn.com/1.jpg", "sales": 200},
            {"name": "Leather Bag", "image": "https://cdn.com/2.jpg", "sales": 160},
        ]
        top_transactions = [
            {
                "customer": { "id": "#23492", "name": "Jenny Wilson" },
                "item": "Leather Bag",
                "date": "2025-06-23",
                "purchase": 2548,
                "status": "live order"
            }
        ]

        return JsonResponse({
            "stats": {
                "revenue": {"value": total_profit, "change": 10},  # Add logic for change if needed
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


    return render(request, 'analytics.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})



def dashboard(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    # Count total image URLs in all documents that are not yet downloaded
    image_docs = DB.images_download.find({"is_downloaded": False})
    image_count = sum(len(doc.get("image_urls", [])) for doc in image_docs)

    # Count total video documents not downloaded (1 video per doc)
    video_count = DB.videos_download.count_documents({"is_downloaded": False})

    collection = DB.products_sold  # your collection

    pipeline = [
        {
            "$group": {
                "_id": "$product_id",  # Group by ObjectId of the product
                "total_quantity": { "$sum": 1 },
                "average_price": { "$avg": "$discounted_amount" },
                "product_name": { "$first": "$product_name" },
                "image": { "$first": { "$arrayElemAt": ["$product_result_images", 0] } }
            }
        },
        { "$sort": SON([("total_quantity", -1)]) },
        { "$limit": 5 }
    ]

    top_selling = list(collection.aggregate(pipeline))

    if user_type == 'Employee':
        return render(request, 'barcode.html', {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})

    return render(request, 'dashboard.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'image_count': image_count, 'video_count': video_count, "top_selling_products": top_selling})

def download_images_zip(request):
    # 1. Fetch all image documents that are not downloaded
    image_docs = list(DB.images_download.find({"is_downloaded": False}))

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
    # 1. Fetch all video documents not yet downloaded
    video_docs = list(DB.videos_download.find({"is_downloaded": False}))

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
                    ext = video_url.split(".")[-1].split("?")[0]  # Remove any query string
                    filename = f"video_{idx+1}.{ext}"
                    zip_file.writestr(filename, response.content)
                else:
                    print(f"Failed to fetch {video_url}: Status {response.status_code}")
            except Exception as e:
                print(f"Error downloading {video_url}: {e}")

    # 3. Mark all fetched video docs as downloaded
    DB.videos_download.update_many({"is_downloaded": False}, {"$set": {"is_downloaded": True}})

    # 4. Send zip file as download response
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.read(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="videos_download.zip"'
    return response


@csrf_exempt
def products_add(request):
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
            products_name = request.POST.get("product_name")
            products_doc = DB.products.find_one({"product_name": products_name})
            if not products_doc:

                products_name = request.POST.get("product_name")
                products_quantity = request.POST.get("quantity")
                products_cost_price = request.POST.get("cost_price")
                products_selling_price = request.POST.get("selling_price")
                products_expiry_date = request.POST.get("expiry_date")
                products_barcode = request.POST.get("barcode")
                products_image = request.POST.get("img")

                products_profit = (int(products_selling_price) - int(products_cost_price)) * int(products_quantity)

                a = request.GET.get('q', '')

                products_dict = {
	                "product_name": products_name,
	                "bought_quantity": products_quantity,
	                "left_quantity": products_quantity,
	                "cost_price": products_cost_price,
	                "selling_price": products_selling_price,
	                "expiry_date": products_expiry_date,
	                "profit": products_profit,
	                "barcode": products_barcode,
	                "image": products_image,
                    "user_id": ObjectId(a),

	            }
                DB.products.insert_one(products_dict)

                products_details1 = list(DB.products.find({'user_id': ObjectId(a)}))

                return render(request, 'products.html',  { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name,  'products_details': products_details1})
                
            else:
                raise Exception
            
        except:
            messages.warning(request, "Already Registered")
            return render(request, 'products_add.html',  { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})
            
    else:
        return render(request, 'products_add.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})



def products(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')
     
    if user_type == "Admin":
    
        b = request.GET.get('q', '')
        users_doc = DB.users.find_one({"email": b})
        product_user_id = users_doc['_id']
        
        products_details1 = list(DB.products.find({'user_id': product_user_id}))

        return render(request, 'products.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'products_details': products_details1, "users_id": product_user_id})
    
    elif user_type == "Shop Owners":
        user_email = data.get('email')
        users_doc = DB.users.find_one({"email": user_email})
        product_user_id = users_doc['_id']

        products_details = list(DB.products.find({'user_id': product_user_id}))

        return render(request, 'products.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'products_details': products_details, "users_id": product_user_id})




def products_sold(request):
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

    products_doc = list(DB.products_sold.find({'user_id': users_id_doc['_id']}))
    
    return render(request, 'products_sold.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name, 'products_doc': products_doc})



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
	                    "date_time": datetime.now(),
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
            users_doc = DB.users.find_one({"Email": users_email})

            if not users_doc:
                users_firstname = request.POST.get("FirstName")
                users_lastname = request.POST.get("LastName")
                users_shop_name = request.POST.get("ShopName")
                users_shop_address = request.POST.get("ShopAddress")
                users_shop_logo = request.FILES['LogoImage']
                users_garments_type = request.POST.get("GarmentsType")
                users_phone_number = request.POST.get("PhoneNumber")
                instagram_link = request.POST.get("instagram_url")
                users_status_value = request.POST.get("StatusValue")
                users_password = request.POST.get("Password")

                shop_logo_url = upload_image_to_azure(users_shop_logo, blob_name="shop_logo")

                users_dict = {
	                "first_name": users_firstname,
	                "last_name": users_lastname,
	                "mobile": users_phone_number,
	                "status": users_status_value,
	                "garments_type": users_garments_type,
	                "shop_name": users_shop_name,
	                "shop_address": users_shop_address,
	                "shop_logo": shop_logo_url,
	                "email": users_email,
	                "instagram_url": instagram_link,
                    "plan_type": "Free Plan",
                    "credits_given": 50,
                    "credits_used": 50,
	                "password": generate_password(users_password),
	                "user_type": 'Shop Owners',
	            }
                DB.users.insert_one(users_dict)

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
    
    
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@csrf_exempt
def login(request):
    try:
        if request.method == 'POST':
            email = request.POST.get("email")
            login_password = request.POST.get("password")

            user_doc = DB.users.find_one({"email": email})
            # user_doc = DB.users.find_one()
            if user_doc:
                userBytes = login_password.encode('utf-8')
                doc_pass = user_doc['password']
                result = bcrypt.checkpw(userBytes, doc_pass)
                if result:
                    email = user_doc.get("email")
                    user_type = user_doc.get("user_type")
                    first_name = user_doc.get("first_name")
                    user_dict = {
                        "email": email,
                        "user_type": user_type,
                        "first_name": first_name,
                    } 
                    jwt_token = generate_token(user_dict)
                    response = HttpResponseRedirect('/dashboard')
                    response.set_cookie("t", jwt_token)
                    user_doc = DB.users.find_one_and_update({"email": email}, {"$set":{"token":jwt_token}})
                    return response
                else:
                    raise Exception
            else:
                raise Exception

        return render(request, 'login.html', {})
    except:
        messages.warning(request, "Invalid ID or Password")
        logger.error("Failed System of logging in .")
        return render(request, 'login.html')



def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie("t")
    return response
