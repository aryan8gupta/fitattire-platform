from PIL import Image, ImageDraw, ImageFont, ImageOps
from moviepy.editor import ImageClip, CompositeVideoClip, ColorClip
import numpy as np



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
    font_path,
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
        line_height = draw.textsize("A", font=font)[1]

        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            line_width, _ = draw.textsize(test_line, font=font)
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

    img = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    y = (box_height - total_text_height) // 2
    for line in lines:
        line_width, _ = draw.textsize(line, font=font)
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
        font_path,
        canvas_size=(1100, 800),
        logo_size=(120, 120),
        # bg_color=(220, 202, 190)
    ):

    W, H = canvas_size

    # Background gray clip
    # bg = ColorClip(size=(W, H), color=bg_color).set_duration(0.1)
    bg = ImageClip("images/background4.jpg").resize((W, H)).set_duration(0.1)

    # Logo clip (resized bigger)
    logo = ImageClip(logo_path).resize(newsize=logo_size).set_position((20, 20))

    # Create combined text string for below logo
    # combined_text = "\n".join(texts)

    text_clips = []
    line_y_offset = 150  # Start just below the logo

    for line in texts:
        text_img = create_text_image(
            line,
            font_path=font_path,
            fontsize=28,
            box_size=(logo_size[0] + 100, 50),
            color="black",
            align="left",
            padding=2
        )

        text_clip = ImageClip(np.array(text_img)).set_position((20, line_y_offset))
        text_clips.append(text_clip)
        line_y_offset += 55  # 60 (height) + 10 spacing


    fixed_big_width = 550
    fixed_big_height = 800

    big_img = ImageClip(big_image_path)
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

    big_img = big_img.set_position(("center", 0))
    


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
    final = CompositeVideoClip(
        [bg, big_img, logo] + text_clips,
        size=(W, H)
    )

    # Save frame as image
    final.save_frame(output_path)


# === Example usage ===
if __name__ == "__main__":
    # font_path = "/Library/Fonts/OpenSans-Bold.ttf"  # Change if needed
    font_path = "/Library/Fonts/DejaVuSans-Bold.ttf"  # Change if needed

    create_dynamic_photo_with_auto_closeup(
        big_image_path="images/product4.jpg",
        logo_path="images/logo1.png",
        texts=[
            "Price: ₹499",
            "Sizes: S, M, L, XL",
            "Fabric: Cotton"
        ],
        output_path="output/output_image2.png",
        font_path=font_path
    )
