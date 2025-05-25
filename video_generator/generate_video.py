from moviepy.editor import ImageClip, ColorClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
from moviepy.audio.fx.all import audio_fadein
import numpy as np


def create_text_image(
    text,
    font_path,
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
        line_height = draw.textsize("A", font=font)[1]

        # Re-wrap text with the current font size
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

    # Create the final image with transparent background
    img = Image.new("RGBA", (box_width, box_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Start drawing vertically centered
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
            x = padding  # fallback
        draw.text((x, y), line, font=font, fill=color)
        y += line_height

    return img


def safe_image_clip(path, duration, height=720):
    try:
        # Try direct loading — works for normal images
        clip = ImageClip(path).set_duration(duration).resize(height=height)
        _ = clip.get_frame(0)  # Force decode to catch corrupt images
        return clip
    except Exception as e:
        print(f"[!] Direct load failed for {path}, falling back. Reason: {e}")
        # Fallback: use Pillow to safely load and flatten
        img = Image.open(path).convert("RGB")
        img = img.resize((int(img.width * height / img.height), height), Image.BICUBIC)
        temp_path = "temp_safe.jpg"
        img.save(temp_path, format="JPEG", quality=95)
        return ImageClip(temp_path).set_duration(duration).set_position("center")

def generate_video(image_path1, image_path2, image_path3, output_path, title_text1, title_text2, audio_path):
    # Load images safely
    image1 = safe_image_clip(image_path1, 5)
    image2 = safe_image_clip(image_path2, 5)
    image3 = safe_image_clip(image_path3, 5)

    # Generate text overlays
    text_image1 = create_text_image(
        text = "This is a sample text that needs to be wrapped and fit within the box.",
        font_path = "/Library/Fonts/DejaVuSans.ttf",
        fontsize = 50,
        box_size = (500, 100),
        color = "white",
        align = "center",
        padding = 10
    )
    text_image2 = create_text_image(
        text = "New Crop Top ₹499",
        font_path = "/Library/Fonts/DejaVuSans.ttf",
        fontsize = 50,
        box_size = (300, 100),
        color = "white",
        align = "center",
        padding = 10
    )

    text_image_np1 = np.array(text_image1)
    text_image_np2 = np.array(text_image2)


    txt_clip1 = ImageClip(text_image_np1).set_position(("center", "bottom")).set_duration(5)
    txt_clip2 = ImageClip(text_image_np2).set_position(("center", "bottom")).set_duration(5)


    # Optional fade-in
    image1 = image1.fadein(1)
    image2 = image2.fadein(1)
    image3 = image3.fadein(1)

    video_clip1 = CompositeVideoClip([image1, txt_clip1])
    video_clip2 = CompositeVideoClip([image2, txt_clip2])
    video_clip3 = CompositeVideoClip([image3])

    final_video = concatenate_videoclips([video_clip1, video_clip2, video_clip3], method="compose")

    # Add audio
    if audio_path:
        audio = AudioFileClip(audio_path).subclip(46, 46+final_video.duration)
        audio = audio.fx(audio_fadein, 3)
        final_video = final_video.set_audio(audio)

    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        bitrate="3000k"
    )

# Example usage
# generate_video(
#     image_path1="images/product1.png",
#     image_path2="images/product2.png",
#     image_path3="images/product3.png",
#     output_path="output/products_video.mp4",
#     title_text1="New Crop Top ₹499",
#     title_text2="New Set Available Now!",
#     audio_path="audio/Wahran.mp3"
# )

# 1st Video part Ends ----------------------------------------------->

# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->

# 2nd Video part Starts ----------------------------------------------->

# --- CONFIGURATION ---
IMAGE_PATHS = [
    "images/product1.png",
    "images/product2.png",
    "images/product3.png",
    "images/product1.png",
    "images/product2.png",
    "images/product3.png",
    "images/product1.png",
    "images/product2.png",
    "images/product3.png",
    "images/product1.png",
]
TEXTS = [
    "New Crop Top ₹499",
    "Stylish Summer Look",
    "Trendy Sets ₹999",
    "Limited Edition Now",
    "Fresh Stock In",
    "Best Seller Today",
    "Top Rated Pick",
    "Just Dropped",
    "Shop This Look",
    "Final Sale!"
]


VIDEO_WIDTH = 720
VIDEO_HEIGHT = 1280
DURATION_PER_IMAGE = 2
SLIDE_DURATION = 0.5  # shorter transition for faster slide
STILL_DURATION = DURATION_PER_IMAGE - SLIDE_DURATION
TOTAL_DURATION = len(IMAGE_PATHS) * DURATION_PER_IMAGE
BG_COLOR = (245, 245, 220)  # Beige
FPS = 15
IMAGE_SCALE = 0.70  # scale down image size


def create_slide_clip(image_path, duration, text=None):
    img_clip = (ImageClip(image_path)
                .resize(height=int(1280 * IMAGE_SCALE))
                .set_duration(duration))

    bg = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=BG_COLOR, duration=duration)
    centered_img = img_clip.set_position(("center", 220))
    if text:
        text_img = create_text_image(
            text=text,
            font_path="/Library/Fonts/DejaVuSans.ttf",  # or use a valid font path on your OS
            fontsize=60,
            box_size=(700, 70),
            color=(101, 67, 33),  # Dark brown RGB
            align="center",
            padding=10
        )
        text_np = np.array(text_img)
        # text_clip = ImageClip(text_np).set_position(("center", "bottom")).set_duration(duration)
        text_clip = ImageClip(text_np).set_position(("center", 100)).set_duration(duration) 
        return CompositeVideoClip([bg, centered_img, text_clip], size=(VIDEO_WIDTH, VIDEO_HEIGHT)).set_duration(duration)
    else:
        return CompositeVideoClip([bg, centered_img], size=(VIDEO_WIDTH, VIDEO_HEIGHT)).set_duration(duration)

def create_slide_transition(prev_image, next_image):
    img_prev = ImageClip(prev_image).resize(height=int(780 * IMAGE_SCALE)).set_duration(SLIDE_DURATION)
    img_next = ImageClip(next_image).resize(height=int(780 * IMAGE_SCALE)).set_duration(SLIDE_DURATION)

    def prev_pos(t):
        dx = VIDEO_WIDTH * (t / SLIDE_DURATION)
        return (VIDEO_WIDTH // 2 - dx - img_prev.w // 2, VIDEO_HEIGHT // 2 - img_prev.h // 2)

    def next_pos(t):
        dx = VIDEO_WIDTH * (1 - t / SLIDE_DURATION)
        return (VIDEO_WIDTH // 2 + dx - img_next.w // 2, VIDEO_HEIGHT // 2 - img_next.h // 2)

    bg = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=BG_COLOR, duration=SLIDE_DURATION)
    return CompositeVideoClip([
        bg,
        img_prev.set_position(prev_pos),
        img_next.set_position(next_pos)
    ], size=(VIDEO_WIDTH, VIDEO_HEIGHT)).set_duration(SLIDE_DURATION)

# --- MAIN ---
clips = []
num_images = len(IMAGE_PATHS)

# Add first image without transition
clips.append(create_slide_clip(IMAGE_PATHS[0], DURATION_PER_IMAGE, text=TEXTS[0]))

# Add rest with transition + hold
for i in range(1, num_images):
    transition = create_slide_transition(IMAGE_PATHS[i - 1], IMAGE_PATHS[i])
    hold = create_slide_clip(IMAGE_PATHS[i], STILL_DURATION, text=TEXTS[i])
    clips.extend([transition, hold])

final_video = concatenate_videoclips(clips, method="compose")

# Stick Texts Starts ---------------------------------->
fixed_text_img = create_text_image(
    text="New Collections",
    font_path="/Library/Fonts/DejaVuSans-Bold.ttf",
    fontsize=80,
    box_size=(700, 80),
    color=(101, 67, 33),  # dark brown
    align="center",
    padding=10
)
fixed_text_np = np.array(fixed_text_img)
fixed_text_clip = (
    ImageClip(fixed_text_np, transparent=True)
    .set_duration(final_video.duration)
    .set_position(("center", 5))  # Top center
)

# Overlay the fixed text on the full video
final_video = CompositeVideoClip([final_video, fixed_text_clip])
# Stick Texts Ends ---------------------------------->


# Load and trim audio
audio = AudioFileClip("audio/Wahran.mp3").subclip(46, 46 + final_video.duration)
audio = audio.fx(audio_fadein, 2)  # Optional fade-in
final_video = final_video.set_audio(audio)
final_video.write_videofile(
    "output/final_reel.mp4",
    fps=FPS,
    # codec="libx264",
    # audio_codec="aac",  # << this is important to run on QuickTime Player
    bitrate="1000k"
)

# 2nd Video part Ends ----------------------------------------------->

# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->


# 3rd Video part Starts ----------------------------------------------->




# 3rd Video part Ends ----------------------------------------------->

# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
# ----------------------------------------------------------------------->
