import os
from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from PIL import Image, ImageOps

register = template.Library()

@register.simple_tag
def resize_static(image_path, width, height, quality=90):
    """Resizes static images, converts to WebP, and serves from media cache."""
    static_full_path = finders.find(image_path)
    if not static_full_path:
        return f"{settings.STATIC_URL}{image_path}"
    
    cache_dir = os.path.join(settings.MEDIA_ROOT, 'cache', 'static_resized')
    os.makedirs(cache_dir, exist_ok=True)
    
    name = os.path.splitext(os.path.basename(image_path))[0]
    new_filename = f"{name}_{width}x{height}_q{quality}.webp"
    new_file_path = os.path.join(cache_dir, new_filename)
    new_file_url = f"{settings.MEDIA_URL}cache/static_resized/{new_filename}"
    
    if not os.path.exists(new_file_path):
        try:
            img = Image.open(static_full_path)
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            img = ImageOps.fit(img, (int(width), int(height)), Image.Resampling.LANCZOS)
            img.save(new_file_path, 'WEBP', quality=int(quality))
        except Exception:
            return f"{settings.STATIC_URL}{image_path}"
            
    return new_file_url
