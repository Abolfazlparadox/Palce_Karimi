import os
from uuid import uuid4
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

def optimize_image(image_field, max_size=(800, 800), quality=85):
    """Resizes and converts images to WebP format for high performance."""
    if not image_field:
        return image_field
        
    img = Image.open(image_field)
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    output = BytesIO()
    img.save(output, format='WebP', quality=quality)
    output.seek(0)
    
    file_name = image_field.name.split('/')[-1].split('.')[0]
    return ContentFile(output.read(), name=f"{file_name}.webp")

def product_image_path(instance, filename):
    return f"products/{instance.product.sku}/{uuid4().hex}.webp"

def variant_image_path(instance, filename):
    return f"variants/{instance.variant.product.sku}/{uuid4().hex}.webp"
