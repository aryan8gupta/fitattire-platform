# from PIL import Image, ImageDraw, ImageFont
# import os

# def create_custom_watermark(text_lines, filename, font_size=40, opacity=100, tilt=30, color=(255, 0, 0)):
#     """Create a transparent watermark image with multiple text lines."""
#     width, height = 800, 400
#     watermark = Image.new("RGBA", (width, height), (0, 0, 0, 0))
#     draw = ImageDraw.Draw(watermark)

#     try:
#         font = ImageFont.truetype("arial.ttf", font_size)
#     except IOError:
#         font = ImageFont.load_default()

#     y_text = 0
#     for line in text_lines:
#         text_width, text_height = draw.textsize(line, font=font)
#         draw.text(((width - text_width) / 2, y_text), line, font=font, fill=color + (opacity,))
#         y_text += text_height + 10

#     watermark = watermark.rotate(tilt, expand=1)
#     watermark.save(filename, "PNG")
#     return filename


# def apply_watermark_avoiding_face(input_image_path, output_image_path, watermark_path, face_area=(50, 50, 250, 250), scale=1.5):
#     """
#     Apply watermark avoiding a specified face/photo area.
#     face_area = (left, top, right, bottom) coordinates in pixels where face is located.
#     """
#     base_image = Image.open(input_image_path).convert("RGBA")
#     watermark = Image.open(watermark_path).convert("RGBA")

#     # Scale watermark
#     w_width = int(base_image.width * scale)
#     w_height = int(watermark.height * (w_width / watermark.width))
#     watermark = watermark.resize((w_width, w_height), Image.LANCZOS)

#     transparent = Image.new("RGBA", base_image.size)
#     transparent.paste(base_image, (0, 0))

#     # Loop over positions (tile-style)
#     step_x = watermark.width // 2
#     step_y = watermark.height // 2
#     for y in range(0, base_image.height, step_y):
#         for x in range(0, base_image.width, step_x):
#             # Skip if watermark would overlap face area
#             wm_box = (x, y, x + watermark.width, y + watermark.height)
#             if not (
#                 wm_box[2] > face_area[0] and
#                 wm_box[0] < face_area[2] and
#                 wm_box[3] > face_area[1] and
#                 wm_box[1] < face_area[3]
#             ):
#                 transparent.paste(watermark, (x, y), mask=watermark)

#     transparent = transparent.convert("RGB")
#     transparent.save(output_image_path)
#     return output_image_path


# if __name__ == "__main__":
#     # 1. Create watermark
#     watermark_file = "aryan_gupta_watermark.png"
#     create_custom_watermark(
#         [
#             "FOR OPENAI ORGANIZATION VERIFICATION ONLY",
#             "ISSUED TO: ARYAN GUPTA",
#             "NOT VALID FOR ANY OTHER PURPOSE"
#         ],
#         filename=watermark_file,
#         font_size=80,
#         opacity=90,
#         tilt=30,
#         color=(255, 0, 0)
#     )

#     # 2. Apply to driving licence (update with your actual file path)
#     input_id_image = "images/driving_license.png"   # your scan
#     output_id_image = "driving_license_watermarked_3.jpg"

#     # Face/photo area (adjust to your document layout)
#     face_box = (50, 50, 250, 250)  # left, top, right, bottom in pixels

#     apply_watermark_avoiding_face(
#         input_image_path=input_id_image,
#         output_image_path=output_id_image,
#         watermark_path=watermark_file,
#         face_area=face_box,
#         scale=0.8
#     )

#     print(f"Watermarked file saved at: {os.path.abspath(output_id_image)}")




from PIL import Image, ImageDraw, ImageFont
import os

def create_watermark_tile(text, font_size=25, opacity=120, color=(255, 0, 0), tilt=30):
    """Create a small diagonal watermark tile with full text visible."""
    # Temporary image to measure text size
    temp_img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    draw_temp = ImageDraw.Draw(temp_img)

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except:
        font = ImageFont.load_default()

    tw, th = draw_temp.textsize(text, font=font)

    # Add padding so rotation doesn't cut text
    tile_w, tile_h = tw + 40, th + 40
    tile = Image.new("RGBA", (tile_w, tile_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tile)

    draw.text(((tile_w - tw) // 2, (tile_h - th) // 2), text, font=font, fill=color + (opacity,))
    tile = tile.rotate(tilt, expand=1)
    return tile

def apply_tiled_watermark(input_image_path, output_image_path, text):
    base = Image.open(input_image_path).convert("RGBA")
    tile = create_watermark_tile(text)

    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    for y in range(0, base.height, tile.height):
        for x in range(0, base.width, tile.width):
            layer.paste(tile, (x, y), mask=tile)

    result = Image.alpha_composite(base, layer).convert("RGB")
    result.save(output_image_path, quality=95)
    print(f"Saved watermarked image to: {os.path.abspath(output_image_path)}")

if __name__ == "__main__":
    wm_text = "FOR OPENAI PERSONA VERIFICATION ONLY"

    input_image = "images/driving_licence.png"      # change to your file
    output_image = "images/dl_watermarked.jpg"

    apply_tiled_watermark(input_image, output_image, wm_text)
