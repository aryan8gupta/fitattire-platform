from moviepy.editor import ImageClip, ColorClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip, vfx
from moviepy.video.fx.crop import crop
from PIL import Image, ImageDraw, ImageFont
from moviepy.audio.fx.all import audio_fadein
import numpy as np
from Inventify.utils.blob_utils import upload_video_to_azure
import random

import os
from Inventify.settings import BASE_DIR

import requests
import tempfile
from io import BytesIO


font_path = os.path.join(BASE_DIR, 'static/assets/fonts/DejaVuSans-Bold.ttf')


def create_text_box(text, font_path, font_size, box_size=(800, 100), text_color="black", box_color=(255, 255, 255), padding=10):
    W, H = box_size
    font = ImageFont.truetype(font_path, font_size)
    img = Image.new("RGBA", box_size, box_color)
    draw = ImageDraw.Draw(img)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]
    text_x = (W - text_w) // 2
    text_y = (H - text_h) // 2
    draw.text((text_x, text_y), text, font=font, fill=text_color)
    return img


def create_text_image(
    text,
    fontsize,
    box_size,
    color="white",
    align="center",
    padding=10
):
    box_width, box_height = box_size
    words = text.split()
    temp_img = Image.new("RGB", box_size)
    draw = ImageDraw.Draw(temp_img)

    while True:
        font = ImageFont.truetype(font_path, fontsize)

        # Estimate line height using bounding box
        bbox = draw.textbbox((0, 0), "A", font=font)
        line_height = bbox[3] - bbox[1]
        line_spacing = int(line_height * 0.4)  # ✅ add 40% spacing

        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_bbox = draw.textbbox((0, 0), test_line, font=font)
            test_line_width = test_bbox[2] - test_bbox[0]

            if test_line_width + 2 * padding <= box_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        total_text_height = (line_height + line_spacing) * len(lines) - line_spacing
        if total_text_height + 2 * padding <= box_height or fontsize <= 10:
            break
        fontsize -= 1

    # Create the final image with transparent background
    img = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    y = (box_height - total_text_height) // 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        if align == "center":
            x = (box_width - line_width) // 2
        elif align == "left":
            x = padding
        elif align == "right":
            x = box_width - line_width - padding
        else:
            x = padding

        draw.text((x, y), line, font=font, fill=color)
        y += line_height + line_spacing  # ✅ spacing applied

    return img




# def create_text_image2(
#     text,
#     fontsize,
#     box_size,
#     color="white",
#     align="center",
#     padding=10
# ):
#     box_width, box_height = box_size
#     words = text.split()
#     temp_img = Image.new("RGB", box_size)
#     draw = ImageDraw.Draw(temp_img)

#     while True:
#         font = ImageFont.truetype(font_path, fontsize)

#         # Estimate line height using bounding box
#         bbox = draw.textbbox((0, 0), "A", font=font)
#         line_height = bbox[3] - bbox[1]

#         # Re-wrap text with the current font size
#         lines = []
#         current_line = ""
#         for word in words:
#             test_line = f"{current_line} {word}".strip()
#             test_bbox = draw.textbbox((0, 0), test_line, font=font)
#             test_line_width = test_bbox[2] - test_bbox[0]

#             if test_line_width + 2 * padding <= box_width:
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

#     # Create the final image with transparent background
#     img = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0))
#     draw = ImageDraw.Draw(img)

#     # Start drawing vertically centered
#     y = (box_height - total_text_height) // 2
#     for line in lines:
#         bbox = draw.textbbox((0, 0), line, font=font)
#         line_width = bbox[2] - bbox[0]
#         if align == "center":
#             x = (box_width - line_width) // 2
#         elif align == "left":
#             x = padding
#         elif align == "right":
#             x = box_width - line_width - padding
#         else:
#             x = padding  # fallback
#         draw.text((x, y), line, font=font, fill=color)
#         y += line_height

#     return img







# def create_text_image(
#     text,
#     fontsize,
#     box_size,
#     color="white",
#     align="center",
#     padding=10
# ):
#     box_width, box_height = box_size
#     words = text.split()
#     temp_img = Image.new("RGB", box_size)
#     draw = ImageDraw.Draw(temp_img)

#     while True:
#         font = ImageFont.truetype(font_path, fontsize)
#         line_height = draw.textsize("A", font=font)[1]

#         # Re-wrap text with the current font size
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

#     # Create the final image with transparent background
#     print("900")
#     img = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0))
#     draw = ImageDraw.Draw(img)

#     # Start drawing vertically centered
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
#             x = padding  # fallback
#         draw.text((x, y), line, font=font, fill=color)
#         y += line_height

#     return img


# def safe_image_clip(path, duration, height=720):
#     try:
#         # Try direct loading — works for normal images
#         clip = ImageClip(path).set_duration(duration).resize(height=height)
#         _ = clip.get_frame(0)  # Force decode to catch corrupt images
#         return clip
#     except Exception as e:
#         print(f"[!] Direct load failed for {path}, falling back. Reason: {e}")
#         # Fallback: use Pillow to safely load and flatten
#         img = Image.open(path).convert("RGB")
#         img = img.resize((int(img.width * height / img.height), height), Image.BICUBIC)
#         temp_path = "temp_safe.jpg"
#         img.save(temp_path, format="JPEG", quality=95)
#         return ImageClip(temp_path).set_duration(duration).set_position("center")

# def generate_video(image_path1, image_path2, image_path3, output_path, title_text1, title_text2, audio_path):
#     # Load images safely
#     image1 = safe_image_clip(image_path1, 5)
#     image2 = safe_image_clip(image_path2, 5)
#     image3 = safe_image_clip(image_path3, 5)

#     # Generate text overlays
#     text_image1 = create_text_image(
#         text = "This is a sample text that needs to be wrapped and fit within the box.",
#         fontsize = 50,
#         box_size = (500, 100),
#         color = "white",
#         align = "center",
#         padding = 10
#     )
#     text_image2 = create_text_image(
#         text = "New Crop Top ₹499",
#         fontsize = 50,
#         box_size = (300, 100),
#         color = "white",
#         align = "center",
#         padding = 10
#     )

#     text_image_np1 = np.array(text_image1)
#     text_image_np2 = np.array(text_image2)


#     txt_clip1 = ImageClip(text_image_np1).set_position(("center", "bottom")).set_duration(5)
#     txt_clip2 = ImageClip(text_image_np2).set_position(("center", "bottom")).set_duration(5)


#     # Optional fade-in
#     image1 = image1.fadein(1)
#     image2 = image2.fadein(1)
#     image3 = image3.fadein(1)

#     video_clip1 = CompositeVideoClip([image1, txt_clip1])
#     video_clip2 = CompositeVideoClip([image2, txt_clip2])
#     video_clip3 = CompositeVideoClip([image3])

#     final_video = concatenate_videoclips([video_clip1, video_clip2, video_clip3], method="compose")

#     # Add audio
#     if audio_path:
#         audio = AudioFileClip(audio_path).subclip(46, 46+final_video.duration)
#         audio = audio.fx(audio_fadein, 3)
#         final_video = final_video.set_audio(audio)

#     final_video.write_videofile(
#         output_path,
#         fps=24,
#         codec="libx264",
#         bitrate="3000k"
#     )

# # Example usage
# # generate_video(
# #     image_path1="images/product1.png",
# #     image_path2="images/product2.png",
# #     image_path3="images/product3.png",
# #     output_path="output/products_video.mp4",
# #     title_text1="New Crop Top ₹499",
# #     title_text2="New Set Available Now!",
# #     audio_path="audio/Wahran.mp3"
# # )

# # 1st Video part Ends ----------------------------------------------->

# # ----------------------------------------------------------------------->
# # ----------------------------------------------------------------------->
# # ----------------------------------------------------------------------->
# # ----------------------------------------------------------------------->

# # 2nd Video part Starts ----------------------------------------------->

# # --- CONFIGURATION ---
# IMAGE_PATHS = [
#     "images/product1.png",
#     "images/product2.png",
#     "images/product3.png",
#     "images/product1.png",
#     "images/product2.png",
#     "images/product3.png",
#     "images/product1.png",
#     "images/product2.png",
#     "images/product3.png",
#     "images/product1.png",
# ]
# TEXTS = [
#     "New Crop Top ₹499",
#     "Stylish Summer Look",
#     "Trendy Sets ₹999",
#     "Limited Edition Now",
#     "Fresh Stock In",
#     "Best Seller Today",
#     "Top Rated Pick",
#     "Just Dropped",
#     "Shop This Look",
#     "Final Sale!"
# ]


# VIDEO_WIDTH = 720
# VIDEO_HEIGHT = 1280
# DURATION_PER_IMAGE = 2
# SLIDE_DURATION = 0.5  # shorter transition for faster slide
# STILL_DURATION = DURATION_PER_IMAGE - SLIDE_DURATION
# TOTAL_DURATION = len(IMAGE_PATHS) * DURATION_PER_IMAGE
# BG_COLOR = (245, 245, 220)  # Beige
# FPS = 15
# IMAGE_SCALE = 0.70  # scale down image size


# def create_slide_clip(image_path, duration, text=None):
#     img_clip = (ImageClip(image_path)
#                 .resize(height=int(1280 * IMAGE_SCALE))
#                 .set_duration(duration))

#     bg = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=BG_COLOR, duration=duration)
#     centered_img = img_clip.set_position(("center", 220))
#     if text:
#         text_img = create_text_image(
#             text=text,
#             fontsize=60,
#             box_size=(700, 70),
#             color=(101, 67, 33),  # Dark brown RGB
#             align="center",
#             padding=10
#         )
#         text_np = np.array(text_img)
#         # text_clip = ImageClip(text_np).set_position(("center", "bottom")).set_duration(duration)
#         text_clip = ImageClip(text_np).set_position(("center", 100)).set_duration(duration) 
#         return CompositeVideoClip([bg, centered_img, text_clip], size=(VIDEO_WIDTH, VIDEO_HEIGHT)).set_duration(duration)
#     else:
#         return CompositeVideoClip([bg, centered_img], size=(VIDEO_WIDTH, VIDEO_HEIGHT)).set_duration(duration)

# def create_slide_transition(prev_image, next_image):
#     img_prev = ImageClip(prev_image).resize(height=int(780 * IMAGE_SCALE)).set_duration(SLIDE_DURATION)
#     img_next = ImageClip(next_image).resize(height=int(780 * IMAGE_SCALE)).set_duration(SLIDE_DURATION)

#     def prev_pos(t):
#         dx = VIDEO_WIDTH * (t / SLIDE_DURATION)
#         return (VIDEO_WIDTH // 2 - dx - img_prev.w // 2, VIDEO_HEIGHT // 2 - img_prev.h // 2)

#     def next_pos(t):
#         dx = VIDEO_WIDTH * (1 - t / SLIDE_DURATION)
#         return (VIDEO_WIDTH // 2 + dx - img_next.w // 2, VIDEO_HEIGHT // 2 - img_next.h // 2)

#     bg = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=BG_COLOR, duration=SLIDE_DURATION)
#     return CompositeVideoClip([
#         bg,
#         img_prev.set_position(prev_pos),
#         img_next.set_position(next_pos)
#     ], size=(VIDEO_WIDTH, VIDEO_HEIGHT)).set_duration(SLIDE_DURATION)

# # --- MAIN ---
# clips = []
# num_images = len(IMAGE_PATHS)

# # Add first image without transition
# clips.append(create_slide_clip(IMAGE_PATHS[0], DURATION_PER_IMAGE, text=TEXTS[0]))

# # Add rest with transition + hold
# for i in range(1, num_images):
#     transition = create_slide_transition(IMAGE_PATHS[i - 1], IMAGE_PATHS[i])
#     hold = create_slide_clip(IMAGE_PATHS[i], STILL_DURATION, text=TEXTS[i])
#     clips.extend([transition, hold])

# final_video = concatenate_videoclips(clips, method="compose")

# # Stick Texts Starts ---------------------------------->
# fixed_text_img = create_text_image(
#     text="New Collections",
#     fontsize=80,
#     box_size=(700, 80),
#     color=(101, 67, 33),  # dark brown
#     align="center",
#     padding=10
# )
# fixed_text_np = np.array(fixed_text_img)
# fixed_text_clip = (
#     ImageClip(fixed_text_np, transparent=True)
#     .set_duration(final_video.duration)
#     .set_position(("center", 5))  # Top center
# )

# # Overlay the fixed text on the full video
# final_video = CompositeVideoClip([final_video, fixed_text_clip])
# # Stick Texts Ends ---------------------------------->


# # Load and trim audio
# audio = AudioFileClip("audio/Wahran.mp3").subclip(46, 46 + final_video.duration)
# audio = audio.fx(audio_fadein, 2)  # Optional fade-in
# final_video = final_video.set_audio(audio)
# final_video.write_videofile(
#     "output/final_reel.mp4",
#     fps=FPS,
#     # codec="libx264",
#     # audio_codec="aac",  # << this is important to run on QuickTime Player
#     bitrate="1000k"
# )

# 2nd Video part Ends ----------------------------------------------->

# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->


# 3rd Video part Starts ----------------------------------------------->

def create_title_or_end_clip(
    background_url=None,       # Make optional
    background_color=None,     # New argument
    logo_url=None,
    text_lines=[],
    is_first_clip=False,
    video_size=(1080, 1920),
    font_size=80
):
    W, H = video_size
    os.makedirs("temp_images", exist_ok=True)

    # Download and prepare background
    # bg_response = requests.get(background_url)
    # background = Image.open(BytesIO(bg_response.content)).convert("RGB").resize((W, H))

    if background_color:
        background = Image.new("RGB", (W, H), background_color)
    elif background_url:
        bg_response = requests.get(background_url)
        background = Image.open(BytesIO(bg_response.content)).convert("RGB").resize((W, H))
    else:
        raise ValueError("You must provide either background_color or background_url.")

    # Download and resize logo
    logo_response = requests.get(logo_url)
    logo = Image.open(BytesIO(logo_response.content)).convert("RGBA")
    logo.thumbnail((300, 300), Image.ANTIALIAS)

    # Sizes
    box_width, box_height = int(W * 0.9), int(H * 0.6)
    logo_x = (box_width - logo.width) // 2
    line_y = logo.height + 5
    line_height = (box_height - line_y - 10) // len(text_lines)
    overlay_x = (W - box_width) // 2
    overlay_y = (H - box_height) // 2

    text_clips = []

    for step in range(len(text_lines)):
        # New background + transparent or semi-transparent overlay
        final_img = background.copy().convert("RGBA")
        overlay = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0) if is_first_clip else (0, 0, 0, 0))
        overlay.paste(logo, (logo_x, 20), logo)

        for i in range(step + 1):
            text_content = text_lines[i][0]
            font_size = text_lines[i][1]
            background_color = text_lines[i][2]

            box_size = (box_width, line_height)
            text_img = create_text_image(
                text=text_content,
                fontsize=font_size,
                box_size=box_size,
                align="center",
                color=background_color
            )
            overlay.paste(text_img, (0, line_y + i * line_height), text_img)

        final_img.paste(overlay, (overlay_x, overlay_y), overlay)

        # Save this step image
        step_path = f"temp_images/step_{step}.png"
        final_img.save(step_path)
        text_clips.append(ImageClip(step_path).set_duration(1.3))

    # Combine all 1-second clips
    return concatenate_videoclips(text_clips, method="compose")



# def create_title_or_end_clip_2(
#     background_url,
#     logo_url,
#     text_lines,
#     is_first_clip,
#     video_size=(1080, 1920),
#     duration=5,
#     font_size=80
# ):
#     W, H = video_size

#     # Download and prepare background
#     bg_response = requests.get(background_url)
#     background = Image.open(BytesIO(bg_response.content)).convert("RGB").resize((W, H))

#     # Download and resize logo
#     logo_response = requests.get(logo_url)
#     logo = Image.open(BytesIO(logo_response.content)).convert("RGBA")
#     logo.thumbnail((300, 300), Image.ANTIALIAS)

#     # Create a semi-transparent box (overlay) for text and logo
#     box_width, box_height = int(W * 0.9), int(H * 0.6)
#     # overlay = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 180))
#     if is_first_clip:
#         overlay = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 160))  # Fully transparent
#     else:
#         overlay = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 160))  # Semi-transparent box


#     # Paste logo at top-center of overlay
#     overlay_draw = ImageDraw.Draw(overlay)
#     logo_x = (box_width - logo.width) // 2
#     overlay.paste(logo, (logo_x, 20), logo)

#     # Generate and paste text images line by line
#     text_clips = []
#     line_y = logo.height + 5
#     line_height = (box_height - line_y - 5) // len(text_lines)

#     print("700")
#     for i, line in enumerate(text_lines):
#         text_content = line[0] # Extract the string from the tuple
#         font_size = line[1]    # Extract the font size from the tuple (if applicable, adjust as needed)
#         background_color = line[2] # Extract the background color (if applicable)

#         box_size = (box_width, line_height)
#         text_img = create_text_image(
#             text=text_content,
#             fontsize=font_size,
#             box_size=box_size,
#             align="center",
#             color=background_color
#         )
#         overlay.paste(text_img, (0, line_y + i * line_height), text_img)


#     print("800")
#     # Combine background and overlay
#     final_img = background.convert("RGBA")
#     overlay_x = (W - box_width) // 2
#     overlay_y = (H - box_height) // 2
#     final_img.paste(overlay, (overlay_x, overlay_y), overlay)

#     # Save and convert to MoviePy ImageClip
#     clip_path = "temp_images/intro_or_outro.png"
#     os.makedirs("temp_images", exist_ok=True)
#     final_img.save(clip_path)
#     print("950")

#     image_clip = ImageClip(clip_path, duration=duration)
#     return image_clip


def create_product_name_clip(product_name, bg_color, text_color="white"):
    W, H = 1080, 1920
    os.makedirs("temp_images", exist_ok=True)

    # Step 1: Create full-color background
    background = Image.new("RGB", (W, H), bg_color)

    # Step 2: Create centered text image (transparent)
    text_img = create_text_image(
        text=product_name.upper(),
        fontsize=80,
        box_size=(W, 300),  # Text box size (height of 300 is enough)
        color=text_color,
        align="center"
    )

    # Step 3: Paste text in center of full screen
    y = (H - text_img.height) // 2
    background.paste(text_img, (0, y), text_img)  # Keep transparency

    # Step 4: Save and return MoviePy ImageClip
    temp_path = f"temp_images/product_name_{random.randint(1000,9999)}.png"
    background.save(temp_path)

    return ImageClip(temp_path).set_duration(2.5)



def generate_reel_video(video_groups, output_path, users_shop_address, users_shop_name):
    total_images = sum(len(group["image_urls"]) for group in video_groups)
    print("Total images:", total_images)

    if total_images < 8:
        print("[INFO] Not enough images to generate video.")
        return None

    os.makedirs("temp_images", exist_ok=True)
    clips = []
    print("1")

    # FIRST CLIP: Title page
    first_clip = create_title_or_end_clip(
        background_color="#bf1836",
        logo_url="https://fitattirestorage.blob.core.windows.net/fitattire-assets/Screenshot 2025-06-08 at 7.30.15 PM.png",
        text_lines=[
            ("END OF SEASON SALE", 60, "white"),
            ("20-50% OFF", 80, "yellow"),
            ("Buy 3 Sets, Save More!", 60, "white"),
            ("Extra Discount Applied at Checkout", 50, "white"),
            ("ADD TO YOUR CART NOW", 60, "black")  
        ],
        is_first_clip = True
    )
    print("100")

    # LAST CLIP: End page
    last_clip = create_title_or_end_clip(
        background_color="#0A1F44",
        logo_url="https://fitattirestorage.blob.core.windows.net/fitattire-assets/Screenshot 2025-06-08 at 7.30.15 PM.png",
        text_lines=[
            ("RELAXED AND TRENDY FIT PRODUCTS", 60, "white"),
            ("VISIT OUR SHOP FOR MORE STYLES", 60, "#FFD700"),
            (f"Shop Name: {users_shop_name}", 60, "#FFD700"),
            (f"Shop Address: {users_shop_address}", 60, "#FFD700"),
            ("For More Product Updates", 50, "white"),
            ("Follow us on Instagram & WhatsApp", 50, "white")
        ],
        is_first_clip = False
    )

       # --- Process Each Product Group ---
    for group in video_groups:
        product_name = group["product_name"]
        image_urls = group["image_urls"]

        name_clip = create_product_name_clip(product_name, bg_color="#00008B")  # or any color
        clips.append(name_clip)



        # Process each image in the group
        for url in image_urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                img = Image.open(BytesIO(response.content)).convert("RGB")

                original_w, original_h = img.size

                # === Resize Logic ===
                if original_h >= 1650:
                    # Big image → scale down to 1650px height
                    target_height = 1650
                else:
                    # Small image → scale up to 1450px height
                    target_height = 1450

                # Initial resize to target height (maintain aspect ratio)
                scale = target_height / original_h
                new_w = int(original_w * scale)
                new_h = target_height
                img = img.resize((new_w, new_h), Image.ANTIALIAS)

                # ✅ If it's a small image → reduce width slightly (manually shrink it)
                if original_h < 1650:
                    shrink_ratio = 0.9  # shrink width by 10%
                    shrunk_w = int(img.width * shrink_ratio)
                    img = img.resize((shrunk_w, img.height), Image.ANTIALIAS)

                # === Paste on 1080x1920 background ===
                bg = Image.new("RGB", (1080, 1920), (245, 245, 245))  # Light gray
                x = (1080 - img.width) // 2
                y = (1920 - img.height) // 2
                bg.paste(img, (x, y))

                # === Save and load into MoviePy ===
                temp_path = f"temp_images/image_{random.randint(1000,9999)}.jpg"
                bg.save(temp_path)

                img_clip = ImageClip(temp_path, duration=3)
                zoomed = img_clip.fx(vfx.resize, lambda t: 1 + 0.05 * t).fadein(0.5).fadeout(0.5)
                clips.append(zoomed)

            except Exception as e:
                print(f"[ERROR] Failed to process image: {url} — {e}")


    if not clips:
        print("4")
        print("[ERROR] No valid image clips created.")
        return None

    full_clips = [first_clip] + clips + [last_clip]
    final_video = concatenate_videoclips(full_clips, method="compose")

    # full_clips = [first_clip] + [last_clip]
    # final_video = concatenate_videoclips(full_clips, method="compose")

    audio_paths = [
        "https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/videos/Wahran(PagalWorldl).mp3",
        "https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/videos/breathe-chill-lofi-beats-362644.mp3",
        "https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/audios/background_audio-1.mp3",
        "https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/videos/coffee-bar-chill-lofi-beats-362645.mp3"
    ]

    try:
        # Pick a random audio path from the list
        audio_path = random.choice(audio_paths)

        # Handle HTTP/HTTPS or local file
        if audio_path.startswith("http://") or audio_path.startswith("https://"):
            response = requests.get(audio_path)
            response.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                temp_audio_file.write(response.content)
                temp_audio_path = temp_audio_file.name
        else:
            temp_audio_path = audio_path

        # Attach the audio (match duration from 46s onwards)
        audio = AudioFileClip(temp_audio_path).subclip(52, 52 + final_video.duration)
        final_video = final_video.set_audio(audio)
        print("[INFO] Audio attached:", final_video.audio)
    except Exception as e:
        print(f"[WARNING] Audio load failed: {e}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        final_video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            ffmpeg_params=["-movflags", "faststart"]
        )
        print("[SUCCESS] Video generated at:", output_path)
        return output_path
    except Exception as e:
        print("[ERROR] Failed to write video file:", e)
        return None
    finally:
        for file in os.listdir("temp_images"):
            os.remove(os.path.join("temp_images", file))




def generate_reel_video3(image_urls, output_path, users_shop_address, users_shop_name):
    if len(image_urls) < 3:
        print("[INFO] Not enough images to generate video.")
        return None

    os.makedirs("temp_images", exist_ok=True)
    clips = []
    print("1")

    # FIRST CLIP: Title page
    first_clip = create_title_or_end_clip(
        background_color="#bf1836",
        logo_url="https://fitattirestorage.blob.core.windows.net/fitattire-assets/Screenshot 2025-06-08 at 7.30.15 PM.png",
        text_lines=[
            ("END OF SEASON SALE", 60, "white"),
            ("20-50% OFF", 80, "yellow"),
            ("Buy 3 Sets, Save More!", 60, "white"),
            ("Extra Discount Applied at Checkout", 50, "white"),
            ("ADD TO YOUR CART NOW", 60, "black")  
        ],
        is_first_clip = True
    )
    print("100")

    # LAST CLIP: End page
    last_clip = create_title_or_end_clip(
        background_color="#0A1F44",
        logo_url="https://fitattirestorage.blob.core.windows.net/fitattire-assets/Screenshot 2025-06-08 at 7.30.15 PM.png",
        text_lines=[
            ("RELAXED AND TRENDY FIT PRODUCTS", 60, "white"),
            ("VISIT OUR SHOP FOR MORE STYLES", 60, "#FFD700"),
            (f"Shop Name: {users_shop_name}", 60, "#FFD700"),
            (f"Shop Address: {users_shop_address}", 60, "#FFD700"),
            ("For More Product Updates", 50, "white"),
            ("Follow us on Instagram & WhatsApp", 50, "white")
        ],
        is_first_clip = False
    )


    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img = Image.open(BytesIO(response.content)).convert("RGB")

            # Resize image to fit inside 1080x1920 frame with padding
            max_width = 880
            max_height = 1580
            img.thumbnail((max_width, max_height), Image.ANTIALIAS)

            # Create padded background
            bg = Image.new("RGB", (1080, 1920), (245, 245, 245))  # Light gray background
            x = (1080 - img.width) // 2
            y = (1920 - img.height) // 2
            bg.paste(img, (x, y))

            temp_path = f"temp_images/image_{i}.jpg"
            bg.save(temp_path)
            print("2")

            img_clip = ImageClip(temp_path, duration=5)

            # Resize to **fill** the frame completely
            img_clip = img_clip.resize(width=1280)  # Fill full width

            # Now crop vertically to fit 1920 height (like center cropping)
            if img_clip.h > 1920:
                img_clip = crop(img_clip, width=1080, height=1920, x_center=img_clip.w / 2, y_center=img_clip.h / 2)
            else:
                # Add black bars or background if it's too short — optional
                img_clip = img_clip.resize(height=1920)

            zoomed = img_clip.fx(vfx.resize, lambda t: 1 + 0.05 * t)
            faded = zoomed.fadein(1).fadeout(1)
            print("3")

            clips.append(faded)

        except Exception as e:
            print(f"[ERROR] Failed to process image {url}: {e}")

    if not clips:
        print("4")
        print("[ERROR] No valid image clips created.")
        return None

    full_clips = [first_clip] + clips + [last_clip]
    final_video = concatenate_videoclips(full_clips, method="compose")

    # full_clips = [first_clip] + [last_clip]
    # final_video = concatenate_videoclips(full_clips, method="compose")

    audio_paths = [
        "https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/videos/Wahran(PagalWorldl).mp3",
        "https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/videos/breathe-chill-lofi-beats-362644.mp3",
        "https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/videos/coffee-bar-chill-lofi-beats-362645.mp3"
    ]

    try:
        # Pick a random audio path from the list
        audio_path = random.choice(audio_paths)

        # Handle HTTP/HTTPS or local file
        if audio_path.startswith("http://") or audio_path.startswith("https://"):
            response = requests.get(audio_path)
            response.raise_for_status()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                temp_audio_file.write(response.content)
                temp_audio_path = temp_audio_file.name
        else:
            temp_audio_path = audio_path

        # Attach the audio (match duration from 46s onwards)
        audio = AudioFileClip(temp_audio_path).subclip(46, 46 + final_video.duration)
        final_video = final_video.set_audio(audio)
        print("[INFO] Audio attached:", final_video.audio)
    except Exception as e:
        print(f"[WARNING] Audio load failed: {e}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        final_video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            ffmpeg_params=["-movflags", "faststart"]
        )
        print("[SUCCESS] Video generated at:", output_path)
        return output_path
    except Exception as e:
        print("[ERROR] Failed to write video file:", e)
        return None
    finally:
        for file in os.listdir("temp_images"):
            os.remove(os.path.join("temp_images", file))



# def generate_reel_video_1(image_urls, output_path, audio_path="https://fitattirestorage.blob.core.windows.net/fitattire-assets/output/videos/Wahran(PagalWorldl).mp3"):
#     if len(image_urls) < 3:
#         print("[INFO] Not enough images to generate video.")
#         return None

#     os.makedirs("temp_images", exist_ok=True)
#     clips = []
#     print("1")

#     for i, url in enumerate(image_urls):
#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             img = Image.open(BytesIO(response.content)).convert("RGB")

#             temp_path = f"temp_images/image_{i}.jpg"
#             img.save(temp_path)
#             print("2")

#             img_clip = ImageClip(temp_path, duration=7).resize(height=1920)
#             img_clip = crop(img_clip, width=1080, height=1920, x_center=img_clip.w / 2, y_center=img_clip.h / 2)

#             # ✅ Corrected zoom effect
#             zoomed = img_clip.fx(vfx.resize, lambda t: 1 + 0.02 * t)

#             faded = zoomed.fadein(1).fadeout(1)
#             print("3")

#             clips.append(faded)

#         except Exception as e:
#             print(f"[ERROR] Failed to process image {url}: {e}")

#     if not clips:
#         print("4")
#         print("[ERROR] No valid image clips created.")
#         return None

#     final_video = concatenate_videoclips(clips, method="compose")

#     if audio_path:
#         try:
#             if audio_path.startswith("http://") or audio_path.startswith("https://"):
#                 # Download the file to a temporary location
#                 response = requests.get(audio_path)
#                 response.raise_for_status()

#                 with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
#                     temp_audio_file.write(response.content)
#                     temp_audio_path = temp_audio_file.name
#             else:
#                 temp_audio_path = audio_path

#             # Load and attach audio
#             audio = AudioFileClip(temp_audio_path).subclip(46, 46 + final_video.duration)
#             final_video = final_video.set_audio(audio)
#             print("[INFO] Audio attached:", final_video.audio)

#         except Exception as e:
#             print(f"[WARNING] Audio load failed: {e}")

#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     try:
#         # final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac')
#         final_video.write_videofile(
#             output_path,
#             fps=24,
#             codec='libx264',              # H.264 for max compatibility
#             audio_codec='aac',            # Required by Instagram & browsers
#             temp_audiofile='temp-audio.m4a',
#             remove_temp=True,
#             ffmpeg_params=["-movflags", "faststart"]  # Important for Chrome & streaming
#         )
#         print("[SUCCESS] Video generated at:", output_path)
#         return output_path
#     except Exception as e:
#         print("[ERROR] Failed to write video file:", e)
#         return None
#     finally:
#         # Cleanup downloaded images
#         for file in os.listdir("temp_images"):
#             os.remove(os.path.join("temp_images", file))


def start_video_generation(video_groups, video_output_path, users_shop_address, users_shop_name):
    try:
        print("[INFO] Background video generation started...")
        local_video_path = generate_reel_video(video_groups, video_output_path, users_shop_address, users_shop_name)
        print("6571")
        if local_video_path:
            print("[SUCCESS] Video saved locally at:", local_video_path)
            return local_video_path

        else:
            print("[ERROR] No video path returned.")
            return None

    except Exception as e:
        print("[CRITICAL] Video generation failed in background:", e)


# 3rd Video part Ends ----------------------------------------------->

# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->

# 4th video part starts -->

def start_video_generation_2(video_groups, video_output_path, users_shop_address, users_shop_name):
    try:
        print("[INFO] Background video generation started...")
        local_video_path = generate_reel_video(video_groups, video_output_path, users_shop_address, users_shop_name)
        print("6571")
        if local_video_path:
            print("[SUCCESS] Video saved locally at:", local_video_path)
            return local_video_path

        else:
            print("[ERROR] No video path returned.")
            return None

    except Exception as e:
        print("[CRITICAL] Video generation failed in background:", e)



# 5th video part starts ------------------>

# def start_video_generation_3(video_groups, video_output_path, users_shop_address, users_shop_name):
#     try:
#         print("[INFO] Background video generation started...")
#         local_video_path = create_reel(video_groups, video_output_path, users_shop_address, users_shop_name)
#         print("6571")
#         if local_video_path:
#             print("[SUCCESS] Video saved locally at:", local_video_path)
#             return local_video_path

#         else:
#             print("[ERROR] No video path returned.")
#             return None

#     except Exception as e:
#         print("[CRITICAL] Video generation failed in background:", e)
