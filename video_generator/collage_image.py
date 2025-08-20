from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import math
from Inventify.utils.blob_utils import upload_image_to_azure
import os
from Inventify.settings import BASE_DIR
import random


FONT_PATH = os.path.join(BASE_DIR, 'static/assets/fonts/DejaVuSans-Bold.ttf')

THEMES = [
    {"bg": (174, 189, 189), "font": "black", "border": "white"},  # grey bg
    {"bg": (255, 228, 196), "font": "black", "border": "brown"},  # bisque
    {"bg": (70, 130, 180), "font": "white", "border": "yellow"},  # steel blue
    {"bg": (240, 248, 255), "font": "black", "border": "navy"},   # alice blue
    {"bg": (47, 79, 79), "font": "white", "border": "cyan"},      # dark slate gray

    {"bg": (25, 25, 112), "font": "white", "border": "gold"},      # midnight blue
    {"bg": (72, 61, 139), "font": "white", "border": "violet"},    # dark slate blue
    {"bg": (0, 100, 0), "font": "white", "border": "lime"},        # dark green
    {"bg": (105, 105, 105), "font": "white", "border": "orange"},  # dim gray
    {"bg": (139, 0, 0), "font": "white", "border": "yellow"},      # dark red
]

def load_image(path_or_url):
    try:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            # Load from URL
            response = requests.get(path_or_url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGBA")
        else:
            # Load from local file
            img = Image.open(path_or_url).convert("RGBA")
        return img
    except Exception as e:
        print(f"Failed to load {path_or_url}: {e}")
        placeholder = Image.new("RGBA", (600, 700), (200, 200, 200, 255))
        draw = ImageDraw.Draw(placeholder)
        draw.text((10, 10), "Image\nnot\navailable", fill="red")
        return placeholder


def create_collage(image_urls, watermark_logo_path):
    canvas_width, canvas_height = 1080, 1080

    # Pick a random theme
    theme = random.choice(THEMES)
    background_color = theme["bg"]
    font_color = theme["font"]
    border_color = theme["border"]

    collage = Image.new("RGBA", (canvas_width, canvas_height), background_color)
    draw = ImageDraw.Draw(collage)

    num_images = len(image_urls)
    max_cols = 3
    spacing = 20
    grid_top_margin = 40
    text_area_height = 150

    rows = math.ceil(num_images / max_cols)
    box_width = (canvas_width - (max_cols + 1) * spacing) // max_cols

    # Box height based on number of images
    if num_images <= 3:
        box_height = int(box_width * 2.2)   # Bigger boxes for <=3 images
    elif 4 <= num_images <= 6:
        box_height = int(box_width * 1.2)
    else:
        available_height = canvas_height - grid_top_margin - text_area_height - (rows + 1) * spacing
        box_height = available_height // rows

    grid_height = rows * box_height + (rows + 1) * spacing
    grid_y = grid_top_margin
    actual_cols = min(num_images, max_cols)
    grid_width = actual_cols * box_width + (actual_cols + 1) * spacing

    extra_margin = 15
    grid_border_thickness = 4

    # If fewer than max_cols (1 or 2 images), center the grid and border
        # If fewer than max_cols (1 or 2 images), center the grid and border
    if num_images < max_cols:
        grid_x_start = (canvas_width - grid_width) // 2
    else:
        grid_x_start = spacing

    # Clamp right edge so it never exceeds canvas_width - extra_margin
    grid_border_rect = [
        grid_x_start - grid_border_thickness,
        grid_y - grid_border_thickness,
        min(grid_x_start + grid_width + grid_border_thickness - 1, canvas_width - 1 - extra_margin),
        grid_y + grid_height + grid_border_thickness - 1,
    ]
    draw.rectangle(grid_border_rect, outline=border_color, width=grid_border_thickness)

    # Font
    base_font_size = 30
    font_size = int(base_font_size * 1.2)
    try:
        font_large = ImageFont.truetype(FONT_PATH, font_size)
    except OSError:
        font_large = ImageFont.load_default()

    # Paste images
    for idx, img_url in enumerate(image_urls):
        img = load_image(img_url)

        # Resize image properly to fit into box
        img_ratio = img.width / img.height
        box_ratio = (box_width - 8) / (box_height - 8)

        if img_ratio > box_ratio:
            new_width = box_width - 8
            new_height = int(new_width / img_ratio)
        else:
            new_height = box_height - 8
            new_width = int(new_height * img_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)

        row = idx // max_cols
        col = idx % max_cols

        if row == rows - 1 and num_images % max_cols != 0:
            last_row_count = num_images % max_cols
            total_last_row_width = last_row_count * box_width + (last_row_count + 1) * spacing
            start_x = (canvas_width - total_last_row_width) // 2 + spacing
            box_x = start_x + col * (box_width + spacing)
        else:
            box_x = grid_x_start + col * (box_width + spacing)

        box_y = grid_y + row * (box_height + spacing)

        # Outer + inner box
        box = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 255))
        inner_box = Image.new("RGBA", (box_width - 4, box_height - 4), (255, 255, 255, 255))
        box.paste(inner_box, (2, 2))

        img_x = (inner_box.width - img.width) // 2 + 2
        img_y = (inner_box.height - img.height) // 2 + 2
        box.paste(img, (img_x, img_y), img)

        collage.paste(box, (box_x, box_y))

    # Watermark
    watermark = load_image(watermark_logo_path)
    watermark_width, watermark_height = watermark.size
    watermark_position = (canvas_width - watermark_width - 20, canvas_height - watermark_height - 20)
    collage.paste(watermark, watermark_position, watermark)

    # Text
    text_y_start = grid_y + grid_height + 20
    avail_text = f"Available in {num_images} colours"
    avail_text_width = draw.textlength(avail_text, font=font_large)
    avail_text_x = (canvas_width - avail_text_width) // 2
    draw.text((avail_text_x, text_y_start), avail_text, font=font_large, fill=font_color)

    order_text = "ORDER NOW"
    order_text_width = draw.textlength(order_text, font=font_large)
    padding_x, padding_y = 25, 12
    box_width_btn = order_text_width + 2 * padding_x
    box_height_btn = font_size + 2 * padding_y
    box_x_btn = (canvas_width - box_width_btn) // 2
    box_y_btn = text_y_start + font_size + 25
    draw.rectangle([box_x_btn, box_y_btn, box_x_btn + box_width_btn, box_y_btn + box_height_btn], fill="white")
    draw.text((box_x_btn + padding_x, box_y_btn + padding_y), order_text, font=font_large, fill="black")

    # Save to in-memory buffer
    img_bytes = BytesIO()
    collage.convert("RGB").save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    # Upload to Azure
    azure_url = upload_image_to_azure(img_bytes, blob_name="tempfiles")
    print(f"Collage uploaded to Azure: {azure_url}")
    return azure_url



# if __name__ == "__main__":
#     image_urls = [
#         "https://fitattirestorage.blob.core.windows.net/fitattire-assets/women:suits:straight-suits:straight-suits-1.png",
#         "https://fitattirestorage.blob.core.windows.net/fitattire-assets/women:suits:straight-suits:straight-suits-4.png",
#         "https://fitattirestorage.blob.core.windows.net/fitattire-assets/women:suits:straight-suits:straight-suits-3.png",
#         "https://fitattirestorage.blob.core.windows.net/fitattire-assets/women:suits:straight-suits:straight-suits-2.png",
#         "images/product-1.png",
#     ]
#     watermark_logo_path = "images/km_fashion-3.png"
#     create_collage(image_urls, "images/collage-1.jpg", watermark_logo_path)
