from PIL import Image


def optimize_image(image_path, max_size=(800, 800)):
    img = Image.open(image_path)

    # Resize while maintaining aspect ratio
    img.thumbnail(max_size)

    # JPG compatibility
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    # Compress
    img.save(
        image_path,
        optimize=True,
        quality=85
    )