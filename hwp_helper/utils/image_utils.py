"""Image processing utilities."""

from PIL import Image, ImageChops
from typing import Optional


def crop_background(image_path: str) -> Optional[Image.Image]:
    """Crop background of an image and return the cropped image."""
    try:
        img = Image.open(image_path)
        bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
        diff = ImageChops.difference(img, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        
        if not bbox:
            return None
            
        # Ensure minimum width
        if bbox[2] - bbox[0] < 300:
            bbox = (bbox[0], bbox[1], bbox[0] + 300, bbox[3])
        
        # Add padding
        bbox = (bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2)
        return img.crop(bbox)
        
    except Exception:
        return None
