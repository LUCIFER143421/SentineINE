from PIL import Image
import io
import os


def get_max_image_dimension():
    try:
        return int(os.getenv("MAX_IMAGE_DIMENSION", "768"))
    except ValueError:
        return 768


MAX_IMAGE_DIMENSION = get_max_image_dimension()
MAX_SIZE = (MAX_IMAGE_DIMENSION, MAX_IMAGE_DIMENSION)
QUALITY = 85


def process_image(uploaded_file):
    try:
        image = Image.open(uploaded_file)
        if image.mode != "RGB":
            image = image.convert("RGB")
        original_size = image.size
        image.thumbnail(MAX_SIZE, Image.LANCZOS)
        resized_size = image.size
        print(f"Image processed: {original_size} to {resized_size}")
        return image, original_size, resized_size
    except Exception as e:
        raise ValueError(f"Failed to process image: {str(e)}")


def image_to_bytes(pil_image):
    buffer = io.BytesIO()
    pil_image.save(buffer, format="JPEG", quality=QUALITY)
    buffer.seek(0)
    return buffer.read()
