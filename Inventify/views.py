from django.conf import settings
from bson import ObjectId
from django.contrib import messages;
from django.shortcuts import render, redirect;
from django.http import HttpResponseRedirect

import bcrypt 
import jwt
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
# from Inventify.settings import DB, PUBLIC_KEY, MEDIA_ROOT
from Inventify.deployment import DB, PUBLIC_KEY, MEDIA_ROOT
from .models import YourModel

from PIL import Image, ImageOps
from io import BytesIO
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


my_var = os.getenv('Pincel_API_Key', 'Default Value')

PINCEL_API_URL = "https://pincel.app/api/clothes-swap"
PINCEL_API_KEY = my_var


# QR-Code Generating / Template----------------------------------------------------------->
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

LABEL_WIDTH_MM = 50
LABEL_HEIGHT_MM = 38
PAGE_WIDTH_MM = 210
PAGE_HEIGHT_MM = 297
TOP_MARGIN_MM = 10
LEFT_MARGIN_MM = 10
GAP_MM = 0

def mm_to_pt(mm_val):
    return mm_val * mm

def generate_qr_code(data, filename="temp_qr.png"):
    qr = qrcode.make(data)
    qr.save(filename)
    return filename

def create_vertical_qr_pdf(data_list, output_file="vertical_qr_labels.pdf"):
    c = canvas.Canvas(output_file, pagesize=(mm_to_pt(PAGE_WIDTH_MM), mm_to_pt(PAGE_HEIGHT_MM)))

    label_width = mm_to_pt(LABEL_WIDTH_MM)
    label_height = mm_to_pt(LABEL_HEIGHT_MM)
    x_qr = mm_to_pt(LEFT_MARGIN_MM + 30)  # QR shifted right to make space for text
    x_text = mm_to_pt(LEFT_MARGIN_MM)     # Text on left
    y = mm_to_pt(PAGE_HEIGHT_MM - TOP_MARGIN_MM - LABEL_HEIGHT_MM)

    for i, item in enumerate(data_list):
        product_name = item.get("name", f"Product {i+1}")
        qr_data = item.get("url", "")

        qr_img = generate_qr_code(qr_data)
        c.drawImage(qr_img, x_qr, y, width=label_width, height=label_height)

        # Draw product name text
        c.setFont("Helvetica", 10)
        c.drawString(x_text, y + label_height / 2, product_name)

        y -= (label_height + mm_to_pt(GAP_MM))

        if y < mm_to_pt(10):
            c.showPage()
            y = mm_to_pt(PAGE_HEIGHT_MM - TOP_MARGIN_MM - LABEL_HEIGHT_MM)

    c.save()
    print(f"PDF saved: {output_file}")

# Example with product names
data_list = [
    {"name": "Black T-Shirt", "url": "http://127.0.0.1:8000/product-display/"},
    {"name": "Denim Jeans", "url": "http://127.0.0.1:8000/product-display/"},
    {"name": "Green Kurti", "url": "http://127.0.0.1:8000/product-display/"},
    {"name": "Formal Shirt", "url": "http://127.0.0.1:8000/product-display/"},
    # Add more...
]

# Uncomment this to create pdf.
# create_vertical_qr_pdf(data_list)
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
    token = jwt.encode({"exp": datetime.now() + timedelta(days=7) , **user_dict}, PUBLIC_KEY, algorithm="HS256")
    return token


def verify_token(token):
    
    decoded_token = {}  
    if token:
        try:
            decoded_token = jwt.decode(token, PUBLIC_KEY, algorithms="HS256", options={"verify_exp": False})
        except Exception as e:
            return False, {}
    else:
        return False, {}
    
    return True, decoded_token


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

    return render(request, 'home.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, "env": settings.ENVIRONMENT})


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


def product_display(request):
    valid = False
    data = {}
    if request.COOKIES.get('t'):
        valid, data = verify_token(request.COOKIES['t'])
    dashboard = None
    if valid:
        dashboard = 'dashboard'
	
    user_type = data.get('user_type')
    user_name = data.get('first_name')

    return render(request, 'product_display.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})


    # result = DB.products.find_one({"qrcode_ids": qr_id})
    # product_discount = ((result.product_price - product.selling_price) / product.product_price) * 100

    # if result:
    #     return render(request, 'product_display.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name, "product": result, 'discount': product_discount})
    # else:
    #     messages.warning(request, "Not Found")
    #     return render(request, "dashboard.html")



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

    return render(request, 'exchange.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})


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

    return render(request, 'sales.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})



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
def upload_image(request):

    if request.method == 'POST':
        clothes_category = request.POST.get("category")
        model_image = request.FILES.get('model_image')
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
                print(data2)

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
                        # Save the Upscaled image
                        upscale_image(data2.get('output'), upscaled_path)

                        # First Saving the Result
                        output_path = os.path.join(MEDIA_ROOT, 'api_result.jpg')
                        save_api_result_from_url(data2.get('output'), output_path)


                        # Add path to the response
                        data2['upscaled_path'] = upscaled_path

                        # Get the relative media URL from the file path
                        relative_path = os.path.relpath(upscaled_path, MEDIA_ROOT)  # gives 'upscaled/final_upscaled-5.jpg'
                        data2['upscaled_url'] = request.build_absolute_uri(os.path.join(settings.MEDIA_URL, relative_path))

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

    print("✅ Add Product page started")

    # def generate_products_id(category_name):
    #     prefix = category_name.strip().upper()[:3]
    #     random_part = ''.join(random.choices(string.digits, k=5))
    #     return f"{prefix}-{random_part}"

    if request.method == 'POST':
        try:
            print("🔍 Reading POST data...")

            # ✅ Safely get the data sent as FormData
            json_data1 = request.POST.get('document')
            print("0")
            json_data2 = request.POST.get('selectedmiddlebuttons')
            print("1")

            if not json_data1:
                print("❌ 'document' is missing in POST")
                return JsonResponse({'error': 'Missing product data'}, status=400)

            parsed_data1 = json.loads(json_data1)
            parsed_data2 = json.loads(json_data2) if json_data2 else {}

            # Prepare to save uploaded garment images
            saved_garment_urls = []

            # garment_images in parsed_data1 are currently placeholders (filenames or base64 strings)
            # We replace them with actual saved media URLs after saving files

            # Loop through all garment image files sent with keys 'garment_0', 'garment_1', ...
            for i in range(len(parsed_data1['product_colors'])):
                file_key = f'garment_{i}'
                uploaded_file = request.FILES.get(file_key)

                if uploaded_file:
                    # Save file to media directory
                    # path = default_storage.save(f'garments/{uploaded_file.name}', ContentFile(uploaded_file.read()))
                    # file_url = default_storage.url(path)  # URL to access the image later
                    uploaded_url = upload_image_to_azure(uploaded_file)
                    saved_garment_urls.append(uploaded_url)
                else:
                    # No file sent for this variant, fallback or error handling
                    saved_garment_urls.append('')  # or handle as you prefer



            # Build the variants array
            variants = []
            for i in range(len(parsed_data1['product_colors'])):
                variant = {
                    "color": parsed_data1['product_colors'][i],
                    "garment_image": saved_garment_urls[i],
                    "result_images": parsed_data1['result_images'][i]  # this should be a list of images per color
                }
                variants.append(variant)

            products_dict = {
                "qrcode_ids": parsed_data1['qrcode_ids'],
                "product_gender": parsed_data2['gender'],
                "product_category": parsed_data2['category'],
                "product_subCategory": parsed_data2['subCategory'],
                "product_finalCategory": parsed_data2['finalCategory'],
                "product_swapCategory": parsed_data2['swapCategory'],
                "brand_name": parsed_data1['brand_name'],
                "product_name": parsed_data1['product_name'],
                "product_quantity": parsed_data1['product_quantity'],
                "sizes": parsed_data1['product_sizes'],
                "product_price": parsed_data1['product_price'],
                "selling_price": parsed_data1['product_selling_price'],
                "variants": variants
            }
            print("2")
            DB.products.create_index({"qrcode_ids": 1})
            print("3")
            DB.products.insert_one(products_dict)
            print("✅ Product inserted successfully")

            return JsonResponse({'uploaded_urls': "uploaded"})

        except:
            messages.warning(request, "Already Registered")
            return render(request, 'add_products.html',  { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})

            

    return render(request, 'add_products.html',  {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})


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
    if user_type == 'Employee':
        return render(request, 'barcode.html', {'dashboard': dashboard, 'user_type': user_type, 'first_name': user_name})

    return render(request, 'dashboard.html', { 'dashboard': 
													   dashboard, 'user_type': user_type, 'first_name': user_name})




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
                users_garments_type = request.POST.get("GarmentsType")
                users_phone_number = request.POST.get("PhoneNumber")
                users_status_value = request.POST.get("StatusValue")
                users_password = request.POST.get("Password")

                users_dict = {
	                "first_name": users_firstname,
	                "last_name": users_lastname,
	                "mobile": users_phone_number,
	                "status": users_status_value,
	                "garments_type": users_garments_type,
	                "shop_name": users_shop_name,
	                "shop_address": users_shop_address,
	                "email": users_email,
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
