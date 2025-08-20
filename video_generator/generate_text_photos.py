import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageColor
from moviepy.editor import ImageClip, CompositeVideoClip, ColorClip
import numpy as np
from io import BytesIO
import random
from Inventify.utils.blob_utils import upload_image_to_azure, download_and_decrypt_image_from_azure  # your custom utility

import os
from Inventify.settings import BASE_DIR

import re
import uuid
import base64 # Import for encoding/decoding mock data


font_path = os.path.join(BASE_DIR, 'static/assets/fonts/DejaVuSans-Bold.ttf')


# Upscale & Remove backround ---------------------------------------->

# from rembg import remove
# import io
# from io import BytesIO
# import requests

# def upscale_image(input_path, output_path, scale_factor=6):
#     with open(input_path, "rb") as input_file:
#         img_bytes = input_file.read()

#         # Convert bytes to a PIL image
#         img = Image.open(BytesIO(img_bytes))

#         new_size = (img.width * scale_factor, img.height * scale_factor)
#         upscaled_img = img.resize(new_size, Image.LANCZOS)
#         upscaled_img.save(output_path)
#         print("Upscaled")

# output_model = "output/model1_no_bg.png"
# result_upscaled_img = "output/upscaled_img.png"

# def remove_background(input_path, output_path):
#     with open(input_path, "rb") as input_file:
#         input_data = input_file.read()
#         output_data = remove(input_data)
#         output_image = Image.open(io.BytesIO(output_data)).convert("RGBA")
#         output_image.save(output_path)
#     # upscale_image(output_path, result_upscaled_img)

# remove_background("images/product3.png", output_model)


def create_text_image(
    text,
    fontsize,
    box_size,
    color="black",
    align="left",
    padding=10
):
    box_width, box_height = box_size
    words = text.split()
    temp_img = Image.new("RGB", box_size)
    draw = ImageDraw.Draw(temp_img)

    while True:
        font = ImageFont.truetype(font_path, fontsize)

        # Estimate line height
        bbox = draw.textbbox((0, 0), "A", font=font)
        line_height = bbox[3] - bbox[1]

        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = test_bbox[2] - test_bbox[0]

            if line_width + 2 * padding <= box_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        total_text_height = line_height * len(lines)
        if total_text_height + 2 * padding <= box_height or fontsize <= 10:
            break
        fontsize -= 1

    # Create the transparent output image
    img = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    y = (box_height - total_text_height) // 2
    for line in lines:
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]

        if align == "center":
            x = (box_width - line_width) // 2
        elif align == "left":
            x = padding
        elif align == "right":
            x = box_width - line_width - padding
        else:
            x = padding

        draw.text((x, y), line, font=font, fill=color)
        y += line_height

    return img


# --- KMS Placeholder Functions (MUST be replaced with your real KMS logic) ---
def encrypt_with_kms(data_to_encrypt):
    if isinstance(data_to_encrypt, str):
        data_bytes = data_to_encrypt.encode('utf-8')
    elif isinstance(data_to_encrypt, bytes):
        data_bytes = data_to_encrypt
    else:
        data_bytes = str(data_to_encrypt).encode('utf-8') # For non-string/bytes, convert to string then bytes
    return b"KMS_ENC_BYTES_" + data_bytes.hex().encode('utf-8') # Mock encryption for bytes

def decrypt_with_kms(encrypted_data_bytes):
    if not isinstance(encrypted_data_bytes, bytes) or not encrypted_data_bytes.startswith(b"KMS_ENC_BYTES_"):
        return encrypted_data_bytes # Not encrypted by this mock function

    return bytes.fromhex(encrypted_data_bytes.replace(b"KMS_ENC_BYTES_", b'').decode('utf-8'))



def upload_image_to_azure_4(file_input, blob_name_prefix=None):
    print(f"[SIMULATED AZURE UPLOAD] Encrypting image locally for mock URL generation: {blob_name_prefix}")
    image_data_bytes = None

    if isinstance(file_input, str):  # Local file path
        with open(file_input, "rb") as f:
            image_data_bytes = f.read()
    elif isinstance(file_input, BytesIO): # BytesIO object
        file_input.seek(0)
        image_data_bytes = file_input.read()
    else:
        raise ValueError("Unsupported file_input type for simulated upload.")

    encrypted_data = encrypt_with_kms(image_data_bytes)
    # Create a mock Azure-like URL containing the base64-encoded encrypted data
    # In a real scenario, this would be a URL pointing to the actual blob in Azure.
    mock_azure_url = f"https://mockstorage.blob.core.windows.net/mockcontainer/{blob_name_prefix}_{uuid.uuid4().hex}.png?encrypted_data={base64.urlsafe_b64encode(encrypted_data).decode('utf-8')}"
    return mock_azure_url

def download_and_decrypt_image_from_azure(encrypted_blob_url):
    print(f"[SIMULATED AZURE DOWNLOAD] Attempting to 'download' and decrypt from mock URL: {encrypted_blob_url}")
    
    # Extract the mock encrypted data from our special URL format
    match = re.search(r'\?encrypted_data=([^&]+)', encrypted_blob_url)
    if not match:
        raise ValueError(f"Mock encrypted URL format invalid: {encrypted_blob_url}")
    
    encoded_encrypted_data = match.group(1)
    encrypted_data = base64.urlsafe_b64decode(encoded_encrypted_data.encode('utf-8'))
    
    plaintext_data = decrypt_with_kms(encrypted_data)
    print(f"[SIMULATED AZURE DOWNLOAD] Decryption successful (length: {len(plaintext_data)})")
    return BytesIO(plaintext_data)



# def load_image_from_path_or_url(image_source):
#     """
#     Loads an image from a local file path or an Azure Blob URL.
#     Assumes internal Azure URLs from your system need decryption,
#     and specific external public URLs do not.
#     Returns a PIL Image object.
#     """
#     # Define known public URLs that do not require decryption.
#     # Add any other static, publicly accessible image URLs here.
#     public_urls = [
#         'https://fitattirestorage.blob.core.windows.net/fitattire-assets/background4.jpg',
#         # Add other specific public asset URLs if your system uses them
#     ]

#     if os.path.exists(image_source):
#         # This path is primarily for local development/testing with actual local files,
#         # or if you ever pass local paths in production.
#         print(f"Loading image from local path: {image_source}")
#         try:
#             return Image.open(image_source).convert("RGBA")
#         except Exception as e:
#             print(f"Error opening local image {image_source}: {e}")
#             raise
#     elif image_source in public_urls:
#         # For known public URLs (like static background images), fetch directly via requests.
#         print(f"Loading image from public URL: {image_source}")
#         try:
#             response = requests.get(image_source)
#             response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
#             return Image.open(BytesIO(response.content)).convert("RGBA")
#         except Exception as e:
#             print(f"Error fetching public image from {image_source}: {e}")
#             raise
#     elif image_source.startswith("http://") or image_source.startswith("https://"):
#         # For any other URL, assume it's an internal Azure Blob URL that needs decryption.
#         print(f"Loading image from internal Azure URL (will attempt decryption): {image_source}")
#         try:
#             # This calls your real blob_utils function that handles Azure download + KMS decryption
#             # image_bytes_io = download_and_decrypt_image_from_azure(image_source)
#             image_bytes_io = image_source
#             return Image.open(image_bytes_io).convert("RGBA")
#         except Exception as e:
#             print(f"ERROR: Failed to download or decrypt image from Azure URL {image_source}: {e}")
#             raise
#     else:
#         raise ValueError(f"Invalid image source: {image_source}. Must be a local path, a known public URL, or an Azure encrypted blob URL.")



def load_image_from_path_or_url(path_or_url):
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        response = requests.get(path_or_url)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    else:
        return Image.open(path_or_url)
    

def crop_and_zoom_upper(image_path, zoom_factor=2):
    img = Image.open(image_path)
    W, H = img.size

    # Crop upper portion more aggressively to zoom more
    crop_height = int(H / zoom_factor)  # Higher zoom_factor = smaller crop, more zoom

    cropped = img.crop((0, 0, W, crop_height))

    zoomed = cropped.resize((W, H), Image.LANCZOS)

    return zoomed



def create_text_image_with_line_spacing(
    text,
    fontsize,
    box_size,
    color="black",
    align="left",
    padding=10,
    wrapped_line_spacing=10  # ✅ This controls space between wrapped lines
):
    box_width, box_height = box_size
    words = text.split()
    temp_img = Image.new("RGB", box_size)
    draw = ImageDraw.Draw(temp_img)

    while True:
        font = ImageFont.truetype(font_path, fontsize)

        # Estimate height of one line
        bbox = draw.textbbox((0, 0), "A", font=font)
        line_height = bbox[3] - bbox[1]

        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_bbox = draw.textbbox((0, 0), test_line, font=font)
            line_width = test_bbox[2] - test_bbox[0]

            if line_width + 2 * padding <= box_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        total_text_height = (
            len(lines) * line_height + (len(lines) - 1) * wrapped_line_spacing
        )

        if total_text_height + 2 * padding <= box_height or fontsize <= 10:
            break
        fontsize -= 1

    # Create final transparent output image
    img = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    y = (box_height - total_text_height) // 2
    for line in lines:
        line_bbox = draw.textbbox((0, 0), line, font=font)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]

        if align == "center":
            x = (box_width - line_width) // 2
        elif align == "left":
            x = padding
        elif align == "right":
            x = box_width - line_width - padding
        else:
            x = padding

        draw.text((x, y), line, font=font, fill=color)
        y += line_height + wrapped_line_spacing  # ✅ apply spacing between lines

    return img



def create_dynamic_photo_with_auto_closeup_1(
        big_image_path,
        logo_path,
        texts,
        output_path,
        canvas_size=(1100, 800),
        logo_size=(200, 130),
    ):

    big_img_pil = load_image_from_path_or_url(big_image_path)
    big_img_np = np.array(big_img_pil)

    logo_img_pil = load_image_from_path_or_url(logo_path)
    logo_img_np = np.array(logo_img_pil)

    background_img_pil = load_image_from_path_or_url(
        'https://fitattirestorage.blob.core.windows.net/fitattire-assets/background4.jpg'
    )
    background_img_np = np.array(background_img_pil)

    W, H = canvas_size

    bg = ImageClip(background_img_np).resize((W, H)).set_duration(0.1)

    # Logo clip
    logo = ImageClip(logo_img_np).resize(newsize=logo_size).set_position((20, 20))

    # Add text clips below the logo
    text_clips = []
    line_y_offset = 150
    text_block_width = 320

    for line in texts:
        text_img = create_text_image_with_line_spacing(
            line,
            fontsize=25,
            box_size=(text_block_width, 140),
            color="black",
            align="left",
            padding=2,
            wrapped_line_spacing=12
        )
        text_clip = ImageClip(np.array(text_img)).set_position((20, line_y_offset))
        text_clips.append(text_clip)
        line_y_offset += 80

    # Prepare big image
    fixed_big_width = 550  # Increased from 400
    fixed_big_height = 800

    big_img = ImageClip(big_img_np)
    original_w, original_h = big_img.w, big_img.h

    large_image_threshold = 3000

    if original_w > large_image_threshold or original_h > large_image_threshold:
        scale = max(fixed_big_width / original_w, fixed_big_height / original_h)
        big_img = big_img.resize(scale).crop(
            x_center=big_img.w // 2,
            y_center=big_img.h // 2,
            width=fixed_big_width,
            height=fixed_big_height
        )
    else:
        scale = min(fixed_big_width / original_w, fixed_big_height / original_h)
        big_img = big_img.resize(scale)

    big_img_clip = big_img.resize((fixed_big_width, fixed_big_height))

    # ✅ Shifted big image towards the right
    margin_right = 120  # Optional margin from the right edge
    big_img_x = W - fixed_big_width - margin_right
    big_img_clip = big_img_clip.set_position((big_img_x, (H - fixed_big_height) // 2))

    # Compose final image
    all_clips = [bg, big_img_clip, logo] + text_clips
    final = CompositeVideoClip(all_clips, size=(W, H))

    frame = final.get_frame(t=0)
    img = Image.fromarray(frame)

    # Save to in-memory buffer
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)


    # # Upload using existing blobs.py utility
    azure_url = upload_image_to_azure(img_bytes, blob_name=output_path)

    return azure_url  # <-- return the blob URL



def create_dynamic_photo_with_auto_closeup_2(
        big_image_path,
        logo_path,
        texts,
        output_path,
        garment_image_path,
        canvas_size=(1100, 800),
        logo_size=(200, 130),
    ):

    big_img_pil = load_image_from_path_or_url(big_image_path)
    big_img_np = np.array(big_img_pil)

    logo_img_pil = load_image_from_path_or_url(logo_path)
    logo_img_np = np.array(logo_img_pil)

    background_img_pil = load_image_from_path_or_url('https://fitattirestorage.blob.core.windows.net/fitattire-assets/background4.jpg')
    background_img_np = np.array(background_img_pil)


    W, H = canvas_size

    bg = ImageClip(background_img_np).resize((W, H)).set_duration(0.1)

    # Logo clip (resized bigger)
    logo = ImageClip(logo_img_np).resize(newsize=logo_size).set_position((20, 20))

    text_clips = []
    line_y_offset = 150  # Start just below the logo
    text_block_width = 260

    for line in texts:
        text_img = create_text_image_with_line_spacing(
            line,
            fontsize=25,
            box_size=(text_block_width, 140),
            color="black",
            align="left",
            padding=2,
            wrapped_line_spacing=12
        )
        text_clip = ImageClip(np.array(text_img)).set_position((20, line_y_offset))
        text_clips.append(text_clip)
        line_y_offset += 80  # 60 (height) + 10 spacing


    fixed_big_width = 400
    fixed_big_height = 800

    big_img = ImageClip(big_img_np)
    original_w, original_h = big_img.w, big_img.h

    # Threshold for "large" images (you can adjust this)
    large_image_threshold = 3000  # width or height bigger than this triggers cropping

    if original_w > large_image_threshold or original_h > large_image_threshold:
        # Large image - fill frame + crop center
        scale_w = fixed_big_width / original_w
        scale_h = fixed_big_height / original_h
        scale = max(scale_w, scale_h)  # cover whole frame
        
        big_img = big_img.resize(scale)
        big_img = big_img.crop(
            x_center=big_img.w // 2, 
            y_center=big_img.h // 2,
            width=fixed_big_width, 
            height=fixed_big_height
        )
    else:
        # Smaller image - fit inside frame without cropping
        scale_w = fixed_big_width / original_w
        scale_h = fixed_big_height / original_h
        scale = min(scale_w, scale_h)  # fit inside frame
        
        big_img = big_img.resize(scale)

    # big_img = big_img.set_position(("center", 0))
    # Position big image on left or center depending on garment_image presence
    # big_img_x = (W - fixed_big_width) // 2 if not garment_image_path else (W - (fixed_big_width * 2 + 60)) // 2

    big_img_clip = big_img.resize((fixed_big_width, fixed_big_height))

    big_img_x = W - fixed_big_width * 2
    big_img_clip = big_img_clip.set_position((big_img_x, (H - fixed_big_height) // 2))

    # ==== Optional Garment Image ====
    garment_clip = None
    if garment_image_path:
        garment_pil = load_image_from_path_or_url(garment_image_path)
        garment_np = np.array(garment_pil)
        garment_clip = ImageClip(garment_np)

        # Resize to match fixed size
        # gw, gh = garment_clip.w, garment_clip.h
        # scale = min(fixed_big_width / gw, fixed_big_height / gh)
        # garment_clip = garment_clip.resize(scale)

        garment_clip = garment_clip.resize((fixed_big_width, fixed_big_height))  # optional: same height


        garment_clip = garment_clip.set_position((
            big_img_x + fixed_big_width,
            (H - fixed_big_height) // 2
        ))


    # Composite all elements
    all_clips = [bg, big_img_clip, logo] + text_clips
    if garment_clip:
        all_clips.append(garment_clip)
    final = CompositeVideoClip(all_clips, size=(W, H))  

    # Get numpy frame
    frame = final.get_frame(t=0)
    img = Image.fromarray(frame)

    # Save to in-memory buffer
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Upload using existing blobs.py utility
    azure_url = upload_image_to_azure(img_bytes, blob_name=output_path)

    return azure_url  # <-- return the blob URL


# New function ----------------------------------------->
def create_offer_photo_with_right_image(
    big_image_path,
    output_path,
    product_id="FiA-75913",
    offer_title="Special Offer",
    discount_text="50% OFF",
    final_line_1="Mention the Product Id",
    final_line_2="Know more.",
    canvas_size=(1080, 1080)
):
    W, H = canvas_size

    # Create background
    colors = [
        (179, 150, 118, 255),  # Brown
        (128, 0, 128, 255),      # Purple
        (0, 100, 0, 255),        # Dark Green
        (0, 0, 139, 255),        # Dark Blue
        (0, 0, 128, 255)         # Navy Blue
    ]

    # # Choose a random color
    bg_color = random.choice(colors)

    # Create new background with randomly chosen color
    bg = Image.new("RGBA", (W, H), bg_color)

    # Load and resize product image
    big_img = load_image_from_path_or_url(big_image_path).convert("RGBA")
    box_width, box_height = 500, 700
    img_with_margin = big_img.resize((box_width - 40, box_height - 60))

    # Create box with border
    box_img = Image.new("RGBA", (box_width, box_height), (255, 255, 255, 0))
    draw_box = ImageDraw.Draw(box_img)
    radius = 30
    draw_box.rounded_rectangle([0, 0, box_width, box_height], radius=radius, outline="white", width=5)
    box_img.paste(img_with_margin, (20, 30), img_with_margin)

    # Paste the image box on the right
    right_margin = 30  # increase this value to move box further left
    box_x = W - box_width - right_margin
    box_y = (H - box_height) // 2
    bg.paste(box_img, (box_x, box_y), box_img)

    # ==== TEXT DRAWING ====
    draw = ImageDraw.Draw(bg)
    font_id = ImageFont.truetype(font_path, 24)
    font_offer = ImageFont.truetype(font_path, 60)
    font_discount = ImageFont.truetype(font_path, 80)
    font_button = ImageFont.truetype(font_path, 28)
    font_final = ImageFont.truetype(font_path, 24)

    # Prepare all text lines
    lines = [
        (f"ID: {product_id}", font_id),
        (offer_title, font_offer),
        (discount_text, font_discount),
        ("", None),  # spacing
        ("Shop Now", font_button),
        ("", None),  # spacing
        (final_line_1, font_final),
        (final_line_2, font_final),
    ]

    # Calculate total height
    total_height = 0
    spacing = 20
    button_padding = (30, 15)
    for text, font in lines:
        if font and text != "Shop Now":
            bbox = font.getbbox(text)
            height = bbox[3] - bbox[1]
            total_height += height + spacing
        elif text == "Shop Now":
            bbox = draw.textbbox((0, 0), text, font=font_button)
            btn_height = (bbox[3] - bbox[1]) + button_padding[1]*2
            total_height += btn_height + spacing
        else:
            total_height += spacing

    start_y = (H - total_height) // 2
    current_y = start_y

    for text, font in lines:
        if text == "":
            current_y += spacing
            continue

        if text == "Shop Now":
            # Draw button
            bbox = draw.textbbox((0, 0), text, font=font_button)
            btn_text_width = bbox[2] - bbox[0]
            btn_text_height = bbox[3] - bbox[1]
            btn_w = btn_text_width + button_padding[0] * 2
            btn_h = btn_text_height + button_padding[1] * 2
            btn_x = 80
            draw.rectangle([btn_x, current_y, btn_x + btn_w, current_y + btn_h], fill="white")
            draw.text(
                (btn_x + button_padding[0], current_y + button_padding[1]),
                text,
                font=font_button,
                fill="black"
            )
            current_y += btn_h + spacing

        else:
            draw.text((80, current_y), text, font=font, fill="white")
            bbox = font.getbbox(text)
            text_height = bbox[3] - bbox[1]
            current_y += text_height + spacing

    # Save and upload image
    img_bytes = BytesIO()
    bg.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    azure_url = upload_image_to_azure(img_bytes, blob_name=output_path)
    return azure_url


# === Function to create the final marketing image ===
def create_offer_photo_with_right_image_2(
    big_image_path,
    output_path,
    logo_path,
    product_name="Cool Shirt",
    product_quantity=2,
    product_selling_price_total_amount="999",
    canvas_size=(1080, 1080),
    product_id="FIA-75913"
):
    W, H = canvas_size
    LEFT_WIDTH = 500  # safe area for logo + text

    # === Background ===
    colors = [
        (179, 150, 118, 255),
        (128, 0, 128, 255),
        (0, 100, 0, 255),
        (0, 0, 139, 255),
        (0, 0, 128, 255)
    ]
    bg_color = random.choice(colors)
    bg = Image.new("RGBA", (W, H), bg_color)
    draw = ImageDraw.Draw(bg)

    # === Fonts ===
    font_large = ImageFont.truetype(font_path, 60)
    font_medium = ImageFont.truetype(font_path, 40)
    font_price = ImageFont.truetype(font_path, 70)
    font_small = ImageFont.truetype(font_path, 26)

    # === Load and resize product image ===
    big_img = load_image_from_path_or_url(big_image_path).convert("RGBA")
    box_width, box_height = 500, 700
    img_with_margin = big_img.resize((box_width - 40, box_height - 60))
    box_img = Image.new("RGBA", (box_width, box_height), (255, 255, 255, 0))
    draw_box = ImageDraw.Draw(box_img)
    draw_box.rounded_rectangle([0, 0, box_width, box_height], radius=30, outline="white", width=5)
    box_img.paste(img_with_margin, (20, 30), img_with_margin)

    # === Paste product image on right ===
    right_margin = 30
    box_x = W - box_width - right_margin
    box_y = (H - box_height) // 2
    bg.paste(box_img, (box_x, box_y), box_img)

    # === Load and resize logo ===
    logo = load_image_from_path_or_url(logo_path).convert("RGBA")
    logo_max_width = 250
    logo_aspect = logo.height / logo.width
    logo = logo.resize((logo_max_width, int(logo_max_width * logo_aspect)))

    # === Text lines (before wrapping) ===
    raw_lines = [
        (f"ID: {product_id}", font_small),
        (f"All New {product_name}", font_medium),
        (f"Buy {product_quantity} Items,", font_medium),
        (f"Just ₹{product_selling_price_total_amount}!", font_price),
        ("DM the Product ID", font_small),
        ("to know more.", font_small),
    ]

    # === Wrap long lines based on LEFT_WIDTH ===
    wrapped_lines = []
    padding = 40
    for text, font in raw_lines:
        words = text.split()
        line = ""
        for word in words:
            test_line = (line + " " + word).strip()
            bbox = draw.textbbox((0, 0), test_line, font=font)
            width = bbox[2] - bbox[0]
            if width <= LEFT_WIDTH - 2 * padding:
                line = test_line
            else:
                if line:
                    wrapped_lines.append((line, font))
                line = word
        if line:
            wrapped_lines.append((line, font))

    # === Measure total content height (logo + wrapped text) ===
    spacing = 20
    total_height = logo.height + spacing
    for line, font in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        total_height += (bbox[3] - bbox[1]) + spacing

    # === Start drawing from vertically centered position ===
    start_y = (H - total_height) // 2
    x = padding
    y = start_y

    # Draw logo
    bg.paste(logo, (x, y), logo)
    logo_bottom_padding = 40
    y += logo.height + logo_bottom_padding


    # Draw each wrapped line
    for line, font in wrapped_lines:

        if "Buy" in line:
            y += 30  # extra space above price
        elif "All" in line:
            y += 10

        draw.text((x, y), line, font=font, fill="white")
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = bbox[3] - bbox[1]

        y += line_height

        # Add extra bottom space if it's the price line
        if "₹" in line:
            y += 40  # <- add extra 40px below price
        else:
            y += spacing  # normal spacing

    # === Save final image ===
    img_bytes = BytesIO()
    bg.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    azure_url = upload_image_to_azure(img_bytes, blob_name=output_path)
    return azure_url



# if __name__ == "__main__":
#     print("--- Starting purely local simulation test ---")
#     print("\nIMPORTANT: This test does NOT interact with Azure. It simulates encryption/decryption locally.")

#     # Ensure local image directories and dummy images exist
#     if not os.path.exists("images"):
#         os.makedirs("images")
#     if not os.path.exists("local_output"):
#         os.makedirs("local_output")
    
#     try:
#         Image.new("RGB", (600, 800), (100, 150, 200)).save("images/product4.jpg")
#         print("Created dummy images/product4.jpg")
#     except Exception as e:
#         print(f"Could not create dummy product4.jpg: {e}. Please ensure PIL is installed and functional.")

#     try:
#         Image.new("RGBA", (200, 100), (0, 0, 0, 255)).save("images/logo1.png") # Black logo
#         print("Created dummy images/logo1.png")
#     except Exception as e:
#         print(f"Could not create dummy logo1.png: {e}. Please ensure PIL is installed and functional.")
    

#     font_dir = os.path.join(mock_settings.BASE_DIR, 'static/assets/fonts')
#     if not os.path.exists(font_dir):
#         os.makedirs(font_dir)
#     font_test_path = os.path.join(font_dir, 'DejaVuSans-Bold.ttf')
#     if not os.path.exists(font_test_path):
#         # You should replace this with a real .ttf font for proper rendering!
#         # For a basic test, even an empty file might work, but text won't draw.
#         with open(font_test_path, "wb") as f:
#             f.write(b'dummy font data') # Minimal dummy content to make ImageFont happy
#         print(f"WARNING: Dummy font file created at {font_test_path}. Replace with actual .ttf for proper rendering.")



#     # --- Step 1: Manually 'upload' local images to get 'mock encrypted URLs' ---
#     # We use upload_image_to_azure to simulate creating the encrypted URL,
#     # but it doesn't actually hit Azure.
#     print("\n--- Simulating 'uploading' local images to get mock encrypted URLs ---")
    
#     # Read local image data into BytesIO to pass to simulated upload
#     with open("images/product4.png", "rb") as f:
#         product_image_data_io = BytesIO(f.read())
#     with open("images/fitattireLogo.png", "rb") as f:
#         logo_image_data_io = BytesIO(f.read())

#     mock_encrypted_product_url = upload_image_to_azure(product_image_data_io, blob_name_prefix="product_sim")
#     print(f"Mock encrypted product image URL: {mock_encrypted_product_url}")

#     mock_encrypted_logo_url = upload_image_to_azure(logo_image_data_io, blob_name_prefix="logo_sim")
#     print(f"Mock encrypted logo image URL: {mock_encrypted_logo_url}")

#     # --- Step 2: Use the *mock encrypted URLs* to generate a new image locally ---
#     # The image generation function will now call load_image_from_path_or_url,
#     # which will then call our simulated download_and_decrypt_image_from_azure.
#     print("\n--- Generating offer photo using mock encrypted URLs (saved locally) ---")
#     final_generated_offer_path = create_offer_photo_with_right_image_2(
#         big_image_path=mock_encrypted_product_url, # Pass the mock encrypted URL
#         logo_path=mock_encrypted_logo_url,        # Pass the mock encrypted URL
#         output_path="generated_offer_test",       # Local filename for output
#         product_id="FiA75913",
#         product_name="Simulated Product",
#         product_quantity=1,
#         product_selling_price_total_amount="1234"
#     )
#     print(f"Final generated offer photo saved to: {final_generated_offer_path}")

#     print("\n--- Generating dynamic photo using mock encrypted URLs (saved locally) ---")
#     final_generated_dynamic_path = create_dynamic_photo_with_auto_closeup_1(
#         big_image_path=mock_encrypted_product_url,
#         logo_path=mock_encrypted_logo_url,
#         texts=[
#             "Price: ₹1234",
#             "Sizes: S, M, L",
#             "Fabric: Cotton",
#             "Color: Blue"
#         ],
#         output_path="generated_dynamic_test",
#     )
#     print(f"Final generated dynamic photo saved to: {final_generated_dynamic_path}")

#     print("\n--- Local simulation test finished ---")
#     print("Check the 'local_output' folder for the generated image files.")




# === Example usage ===
# if __name__ == "__main__":

#     # create_dynamic_photo_with_auto_closeup(
#     #     big_image_path="images/product4.jpg",
#     #     logo_path="images/logo1.png",
#     #     texts=[
#     #         "Price: ₹499",
#     #         "Sizes: S, M, L, XL",
#     #         "Fabric: Cotton"
#     #     ],
#     #     output_path="output/output_image2.png",
#     # )
#     create_offer_photo_with_right_image(
#         big_image_path="images/product4.jpg",
#         logo_path="images/logo1.png",  # not used here but can be reused
#         output_path="generated",
#         product_id="FiA75913"
#     )

