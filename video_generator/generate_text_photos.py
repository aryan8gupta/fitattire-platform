import requests
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageColor
from moviepy.editor import ImageClip, CompositeVideoClip, ColorClip
import numpy as np
from io import BytesIO
import random
from Inventify.utils.blob_utils import upload_image_to_azure  # your custom utility

import os
from Inventify.base import BASE_DIR

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



# def create_text_image(
#     text,
#     fontsize,
#     box_size,
#     color="black",
#     align="left",
#     padding=10
# ):
#     box_width, box_height = box_size
#     words = text.split()
#     temp_img = Image.new("RGB", box_size)
#     draw = ImageDraw.Draw(temp_img)

#     while True:
#         font = ImageFont.truetype(font_path, fontsize)
#         line_height = draw.textsize("A", font=font)[1]

#         lines = []
#         current_line = ""
#         for word in words:
#             test_line = f"{current_line} {word}".strip()
#             line_width, _ = draw.textsize(test_line, font=font)
#             if line_width + 2 * padding <= box_width:
#                 current_line = test_line
#             else:
#                 if current_line:
#                     lines.append(current_line)
#                 current_line = word
#         if current_line:
#             lines.append(current_line)

#         total_text_height = line_height * len(lines)
#         if total_text_height + 2 * padding <= box_height or fontsize <= 10:
#             break
#         fontsize -= 1

#     img = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0))
#     draw = ImageDraw.Draw(img)

#     y = (box_height - total_text_height) // 2
#     for line in lines:
#         line_width, _ = draw.textsize(line, font=font)
#         if align == "center":
#             x = (box_width - line_width) // 2
#         elif align == "left":
#             x = padding
#         elif align == "right":
#             x = box_width - line_width - padding
#         else:
#             x = padding
#         draw.text((x, y), line, font=font, fill=color)
#         y += line_height

#     return img


def make_circle_image(pil_img, size):
    pil_img = pil_img.resize(size).convert("RGBA")
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size[0], size[1]), fill=255)
    result = ImageOps.fit(pil_img, size, centering=(0.5, 0.5))
    result.putalpha(mask)
    return result


# def crop_upper_half_circle_with_transparency(image_path, output_size=(250, 250)):
#     img = Image.open(image_path).convert("RGBA")
#     W, H = img.size
#     cropped = img.crop((0, 0, W, H // 2)).resize(output_size)

#     # Create a circular mask
#     mask = Image.new("L", output_size, 0)
#     draw = ImageDraw.Draw(mask)
#     draw.ellipse((0, 0, output_size[0], output_size[1]), fill=255)

#     # Apply circular mask to create transparency
#     cropped.putalpha(mask)
#     return cropped

# def add_colored_circle_frame(cropped_img, bg_color=(255, 255, 255), padding=10):
#     size_with_padding = (cropped_img.size[0] + 2 * padding, cropped_img.size[1] + 2 * padding)
#     bg = Image.new("RGBA", size_with_padding, bg_color + (255,))
    
#     # Center the circular image on the new background
#     bg.paste(cropped_img, (padding, padding), cropped_img)
#     return bg

# def crop_upper_half(image_path):
#     img = Image.open(image_path)
#     W, H = img.size

#     cropped_img = img.crop((0, 0, W, H // 1.5))  # left, top, right, bottom
#     return cropped_img

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


def create_dynamic_photo_with_auto_closeup(
        big_image_path,
        logo_path,
        texts,
        output_path,
        garment_image_path=None,  # optional
        canvas_size=(1100, 800),
        # canvas_size=(1080, 1080),
        logo_size=(200, 130),
        # bg_color=(220, 202, 190)
    ):

    big_img_pil = load_image_from_path_or_url(big_image_path)
    big_img_np = np.array(big_img_pil)

    logo_img_pil = load_image_from_path_or_url(logo_path)
    logo_img_np = np.array(logo_img_pil)

    background_img_pil = load_image_from_path_or_url('https://fitattirestorage.blob.core.windows.net/fitattire-assets/background4.jpg')
    background_img_np = np.array(background_img_pil)


    W, H = canvas_size

    # Background gray clip
    # bg = ColorClip(size=(W, H), color=bg_color).set_duration(0.1)
    bg = ImageClip(background_img_np).resize((W, H)).set_duration(0.1)

    # Logo clip (resized bigger)
    logo = ImageClip(logo_img_np).resize(newsize=logo_size).set_position((20, 20))

    # Create combined text string for below logo
    # combined_text = "\n".join(texts)

    text_clips = []
    line_y_offset = 150  # Start just below the logo
    text_block_width = 260

    for line in texts:
        text_img = create_text_image(
            line,
            fontsize=28,
            # box_size=(logo_size[0] + 100, 50),
            box_size=(text_block_width, 50),
            color="black",
            align="left",
            padding=2
        )

        text_clip = ImageClip(np.array(text_img)).set_position((20, line_y_offset))
        text_clips.append(text_clip)
        line_y_offset += 55  # 60 (height) + 10 spacing

    # # === Big Image processing ===
    # def prepare_image_clip(np_image, max_w, max_h):
    #     clip = ImageClip(np_image)
    #     ow, oh = clip.w, clip.h
    #     scale = min(max_w / ow, max_h / oh)
    #     return clip.resize(scale)

    # big_img_clip = prepare_image_clip(big_img_np, 350, 700)

    # # === Garment Image (optional) ===
    # garment_clip = None
    # if garment_image_path:
    #     garment_pil = load_image_from_path_or_url(garment_image_path)
    #     garment_np = np.array(garment_pil)
    #     garment_clip = prepare_image_clip(garment_np, 350, 700)

    # # === Positioning logic ===
    # spacing = 30  # space between text+logo and big image
    # spacing2 = 0  # no space between big image and garment image

    # # Width of each section
    # text_block_total_w = text_block_width + 40  # text + margin
    # big_img_w = big_img_clip.w
    # garment_w = garment_clip.w if garment_clip else 0

    # total_required_w = text_block_total_w + spacing + big_img_w + spacing2 + garment_w
    # start_x = (W - total_required_w) // 2

    # # X positions
    # text_x = start_x
    # big_x = text_x + text_block_total_w + spacing
    # garment_x = big_x + big_img_w + spacing2

    # # Y positions
    # big_y = (H - big_img_clip.h) // 2
    # if garment_clip:
    #     garment_y = (H - garment_clip.h) // 2

    # # Set final positions
    # big_img_clip = big_img_clip.set_position((big_x, big_y))
    # if garment_clip:
    #     garment_clip = garment_clip.set_position((garment_x, garment_y))
    # logo = logo.set_position((text_x + 10, 20))
    # for i, clip in enumerate(text_clips):
    #     text_clips[i] = clip.set_position((text_x + 10, 150 + i * 55))



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
    


    # Big image clip on left (~60% width)

    # big_img_width = int(W * 0.5)
    # big_img_max_height = int(H)
    # big_img = ImageClip(big_image_path).resize(width=big_img_width)
    # if big_img.h > big_img_max_height:
    #     big_img = big_img.resize(height=big_img_max_height)
    # big_img = big_img.set_position((240, 10))

    # big_img = big_img.set_position((180, (H - big_img.h) // 2))

    
    # For Circle Frame with image background ----------------------------------------------->
    # cropped_pil_img = crop_upper_half(big_image_path)
    # cropped_pil_img = crop_and_zoom_upper(big_image_path)
    # circle_size = (350, 450)  # Adjust diameter as needed
    # circle_img = make_circle_image(cropped_pil_img, circle_size)


    # # Convert to MoviePy clip
    # small_img_clip = ImageClip(np.array(circle_img)).set_position((
    #     W - circle_size[0] - 10,
    #     (H - circle_size[1]) // 2
    # ))
    # ---------------------------------------------------------------------------------->


    # For Square Frame right image ----------------------------------------------->
    # cropped_pil_img = crop_upper_half(big_image_path)
    # small_img_width = int(W * 0.3)
    # small_img_max_height = int(H * 0.5)
    # cropped_pil_img = cropped_pil_img.resize((small_img_width, small_img_max_height))

    # small_img_clip = ImageClip(np.array(cropped_pil_img)).set_position((W - small_img_width - 40, 20))
    # small_img_clip = ImageClip(np.array(cropped_pil_img)).set_position((
    #     W - small_img_width - 20,
    #     (H - small_img_max_height) // 2
    # ))
    # ---------------------------------------------------------------------------------->


    # For Different-Color Circle frame and remove backround -------------------------->
    # cropped_pil_img = crop_upper_half_circle_with_transparency(big_image_path, output_size=circle_size)
    # framed_circular_img = add_colored_circle_frame(cropped_pil_img, bg_color=(220, 202, 190), padding=8)
    # small_img_clip = ImageClip(np.array(framed_circular_img), ismask=False).set_position((
    #     W - circle_size[0] - 10,
    #     (H - circle_size[1]) // 2
    # ))
    # ---------------------------------------------------------------------------------->


    # Composite all elements
    all_clips = [bg, big_img_clip, logo] + text_clips
    if garment_clip:
        all_clips.append(garment_clip)
    final = CompositeVideoClip(all_clips, size=(W, H))  

    # final = CompositeVideoClip(
    #     [bg, big_img, logo] + text_clips,
    #     size=(W, H)
    # )

    # Save frame as image
    # final.save_frame(output_path)

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


# def create_offer_photo_with_right_image(
#         big_image_path,
#         logo_path,
#         output_path,
#         product_id="FiA75913",
#         canvas_size=(1080, 1080)
#     ):
#     W, H = canvas_size

#     # Load background
#     bg = Image.new("RGBA", (W, H), (179, 150, 118))  # Black background

#     # Load main product image
#     big_img = load_image_from_path_or_url(big_image_path).convert("RGBA")
#     box_width, box_height = 500, 700
#     img_with_margin = big_img.resize((box_width - 40, box_height - 60))  # leave margin

#     # Create box with border
#     box_img = Image.new("RGBA", (box_width, box_height), (255, 255, 255, 0))
#     draw_box = ImageDraw.Draw(box_img)
#     radius = 30
#     draw_box.rounded_rectangle([0, 0, box_width, box_height], radius=radius, outline="white", width=5)

#     # Paste the product image inside the box with margin
#     box_img.paste(img_with_margin, (20, 30), img_with_margin)

#     # Paste box_img on right side of canvas
#     bg.paste(box_img, ((W + 100 - box_width) // 2 + 200, (H - box_height) // 2), box_img)

#     # ==== Text Area ====
#     draw = ImageDraw.Draw(bg)

#     def draw_text_line(text, size, y, bold=False):
#         font = ImageFont.truetype(font_path, size)
#         draw.text((80, y), text, font=font, fill="white")
#         return y + size + 20

#     y_text = 100
#     y_text = draw_text_line(f"ID: {product_id}", 32, y_text)
#     y_text = draw_text_line("Special Offer", 60, y_text)
#     y_text = draw_text_line("50% OFF", 80, y_text)

#     # ==== Shop Now Button ====
#     button_font = ImageFont.truetype(font_path, 36)
#     button_text = "Shop Now"
#     button_padding = (30, 15)
#     text_size = draw.textsize(button_text, font=button_font)
#     btn_w = text_size[0] + button_padding[0] * 2
#     btn_h = text_size[1] + button_padding[1] * 2
#     btn_x = 80
#     btn_y = y_text + 30

#     draw.rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], fill="white", outline=None)
#     draw.text(
#         (btn_x + button_padding[0], btn_y + button_padding[1]),
#         button_text,
#         font=button_font,
#         fill="black"
#     )

#     # ==== Final Line ====
#     final_line = "Mention the product ID to know more."
#     final_font = ImageFont.truetype(font_path, 24)
#     draw.text((80, btn_y + btn_h + 40), final_line, font=final_font, fill="white")

#     # Convert to BytesIO and upload
#     img_bytes = BytesIO()
#     bg.save(img_bytes, format='PNG')
#     img_bytes.seek(0)
#     azure_url = upload_image_to_azure(img_bytes, blob_name=output_path)
#     return azure_url


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

    # if not os.path.exists(output_path):
    #     os.makedirs(output_path)
    # final_path = os.path.join(output_path, f"{product_id}_offer.png")
    # bg.convert("RGB").save(final_path)
    # print(f"✅ Image saved at: {final_path}")


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

