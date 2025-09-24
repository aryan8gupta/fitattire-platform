from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import requests
from io import BytesIO
import math, random
from Inventify.utils.blob_utils import upload_image_to_azure
from Inventify.settings import BASE_DIR
import os

FONT_PATH = os.path.join(BASE_DIR, 'static/assets/fonts/DejaVuSans-Bold.ttf')

# === THEMES ===
THEMES = [
    {
        "background": (245, 240, 235),
        "header_bg": (100, 20, 20), "header_text": "white",
        "footer_bg": (100, 20, 20), "footer_text": "white",
        "logo_color": "purple", "border_color": "black", "label_text": "black"
    },
    {
        "background": (250, 250, 255),
        "header_bg": (0, 102, 204), "header_text": "white",
        "footer_bg": (0, 102, 204), "footer_text": "white",
        "logo_color": "blue", "border_color": "navy", "label_text": "black"
    },
    {
        "background": (255, 245, 240),
        "header_bg": (200, 50, 50), "header_text": "white",
        "footer_bg": (200, 50, 50), "footer_text": "white",
        "logo_color": "red", "border_color": "darkred", "label_text": "black"
    },
    {
        "background": (240, 255, 240),
        "header_bg": (34, 139, 34), "header_text": "white",
        "footer_bg": (34, 139, 34), "footer_text": "white",
        "logo_color": "darkgreen", "border_color": "darkgreen", "label_text": "black"
    },
    {
        "background": (255, 250, 240),
        "header_bg": (255, 140, 0), "header_text": "white",
        "footer_bg": (255, 140, 0), "footer_text": "white",
        "logo_color": "darkorange", "border_color": "orange", "label_text": "black"
    },
    {
        "background": (245, 245, 255),
        "header_bg": (138, 43, 226), "header_text": "white",
        "footer_bg": (138, 43, 226), "footer_text": "white",
        "logo_color": "indigo", "border_color": "purple", "label_text": "black"
    },
    {
        "background": (255, 255, 240),
        "header_bg": (218, 165, 32), "header_text": "black",
        "footer_bg": (218, 165, 32), "footer_text": "black",
        "logo_color": "goldenrod", "border_color": "darkgoldenrod", "label_text": "black"
    },
    {
        "background": (250, 240, 255),
        "header_bg": (199, 21, 133), "header_text": "white",
        "footer_bg": (199, 21, 133), "footer_text": "white",
        "logo_color": "deeppink", "border_color": "mediumvioletred", "label_text": "black"
    },
    {
        "background": (240, 248, 255),
        "header_bg": (70, 130, 180), "header_text": "white",
        "footer_bg": (70, 130, 180), "footer_text": "white",
        "logo_color": "steelblue", "border_color": "navy", "label_text": "black"
    },
    {
        "background": (255, 255, 255),
        "header_bg": (50, 50, 50), "header_text": "white",
        "footer_bg": (50, 50, 50), "footer_text": "white",
        "logo_color": "black", "border_color": "gray", "label_text": "black"
    }
]


# === Compatibility helper for text measurement ===
def measured_text_size(draw, text, font):
    """
    Return (width, height) for text with given draw object and font,
    trying multiple APIs for compatibility across Pillow versions.
    """
    # 1) Prefer draw.textbbox (available in newer Pillow)
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        pass

    # 2) Older Pillow versions may have draw.textsize
    try:
        return draw.textsize(text, font=font)
    except Exception:
        pass

    # 3) Font's own bbox (newer API)
    try:
        bbox = font.getbbox(text)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]
    except Exception:
        pass

    # 4) Older font.getsize
    try:
        return font.getsize(text)
    except Exception:
        pass

    # 5) Fallback to mask
    try:
        mask = font.getmask(text)
        return mask.size
    except Exception:
        pass

    # 6) Give up
    return (0, 0)


# === HERO IMAGE ===
def prepare_hero(path, max_height=1536, sharpen=True):
    if path.startswith("http://") or path.startswith("https://"):
        response = requests.get(path, timeout=10)
        response.raise_for_status()
        hero = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        hero = Image.open(path).convert("RGB")

    if hero.height > max_height:
        aspect = hero.width / hero.height
        new_height = max_height
        new_width = int(aspect * new_height)
        hero = hero.resize((new_width, new_height), Image.Resampling.LANCZOS)

    if sharpen:
        hero = hero.filter(ImageFilter.UnsharpMask(radius=1.2, percent=180, threshold=2))

    return hero


# === COLOUR IMAGE ===
def load_image(path_or_url, size=None, sharpen=False):
    try:
        if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
            response = requests.get(path_or_url, timeout=10)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            img = Image.open(path_or_url).convert("RGB")

        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)

        if sharpen:
            img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=250, threshold=2))

        return img
    except Exception as e:
        print(f"Failed to load {path_or_url}: {e}")
        return Image.new("RGB", size or (300, 300), (200, 200, 200))


# === MAIN ===
def create_saree_catalog_single_image(hero_path, colour_image, fabric, code, price, sharpen=False):

    # Pick a random theme
    theme = random.choice(THEMES)

    # Settings
    padding = 50

    hero = prepare_hero(hero_path, max_height=1536, sharpen=True)

    # Decide size for the single right-hand image:
    # make it ~2/3 of hero width and match hero height
    # single_width = hero.width * 2 // 3
    single_width = hero.width

    single_height = hero.height
    single_size = (single_width, single_height)

    # Canvas dimensions: hero + single image + padding margins
    canvas_width = hero.width + single_width + 4 * padding
    canvas_height = max(hero.height, single_height) + 350  # extra bottom for footer

    collage = Image.new("RGB", (canvas_width, canvas_height), theme["background"])
    draw = ImageDraw.Draw(collage)

    # Fonts
    try:
        font_logo = ImageFont.truetype(FONT_PATH, 52)
        font_header = ImageFont.truetype(FONT_PATH, 42)
        font_footer = ImageFont.truetype(FONT_PATH, 50)
        font_label = ImageFont.truetype(FONT_PATH, 28)
    except Exception:
        font_logo = font_header = font_footer = font_label = ImageFont.load_default()

    # Logo
    logo_text = "KM Sarees"
    lw, lh = measured_text_size(draw, logo_text, font_logo)
    draw.text(((canvas_width - lw) // 2, 10), logo_text, fill=theme["logo_color"], font=font_logo)

    # Paste Hero (left)
    hero_x, hero_y = padding, 180
    collage.paste(hero, (hero_x, hero_y))
    draw.rectangle([hero_x - 5, hero_y - 5, hero_x + hero.width + 5, hero_y + hero.height + 5],
                   outline=theme["border_color"], width=3)

    # Load and place single image (right)
    single_img = load_image(colour_image, size=single_size, sharpen=sharpen)
    single_img = single_img.resize(single_size, Image.Resampling.LANCZOS)

    single_x = hero_x + hero.width + 2 * padding
    single_y = hero_y
    collage.paste(single_img, (single_x, single_y))
    draw.rectangle([single_x - 3, single_y - 3, single_x + single_width + 3, single_y + single_height + 3],
                   outline=theme["border_color"], width=2)

    # # Label under single image (commented out but compatibility-ready)
    # label_text = "Shade / Variant"
    # tw, th = measured_text_size(draw, label_text, font_label)
    # draw.text((single_x + single_width // 2 - tw // 2, single_y + single_height + 8),
    #           label_text, fill=theme["label_text"], font=font_label)

    # Header
    header_text = f"Fabric: {fabric}   |   Code: {code}   |   Price: {price}"
    draw.rectangle([0, 70, canvas_width, 140], fill=theme["header_bg"])
    tw, th = measured_text_size(draw, header_text, font_header)
    draw.text(((canvas_width - tw) // 2, 105 - th // 2),
              header_text, fill=theme["header_text"], font=font_header)

    # Footer
    footer_text = f"Available in Premium Colours"
    draw.rectangle([0, canvas_height - 120, canvas_width, canvas_height], fill=theme["footer_bg"])
    tw, th = measured_text_size(draw, footer_text, font_footer)
    draw.text(((canvas_width - tw) // 2, canvas_height - 80),
              footer_text, fill=theme["footer_text"], font=font_footer)

    # ✅ Ensure WhatsApp HD resolution (longest side >= 3000 px)
    min_hd_size = 3000
    longest = max(collage.width, collage.height)
    if longest < min_hd_size:
        scale = min_hd_size / longest
        new_width = int(collage.width * scale)
        new_height = int(collage.height * scale)
        collage = collage.resize((new_width, new_height), Image.Resampling.LANCZOS)

    img_bytes = BytesIO()
    collage.convert("RGB").save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    # Upload to Azure
    azure_url = upload_image_to_azure(img_bytes, blob_name="generated")
    print(f"Collage uploaded to Azure: {azure_url}")
    return azure_url


# # === Example usage ===
# if __name__ == "__main__":
#     hero_img = "images/hero-1.png"
#     single_colour_img = "images/single_image-1.jpeg"
#     create_saree_catalog_single_image(hero_img, single_colour_img,
#                          fabric="Jackord", code="KAV-05", price="Rs. 4350",
#                          output_path="saree_catalog-single-1.png",
#                          sharpen=True)
