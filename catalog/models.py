from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from .utils import optimize_image, product_image_path, variant_image_path

class ExchangeRate(models.Model):
    currency_code = models.CharField(max_length=3, unique=True, help_text="e.g., USD, IRR, TRY, AED")
    rate_to_base = models.DecimalField(max_digits=20, decimal_places=4, help_text="Exchange rate relative to base currency")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.currency_code

class Category(TranslatableModel):
    is_active = models.BooleanField(default=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=100),
        slug=models.SlugField(allow_unicode=True, unique=True),
        description=models.TextField(blank=True)
    )

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Unnamed Category"

class Product(TranslatableModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=200),
        slug=models.SlugField(allow_unicode=True, unique=True),
        short_description=models.TextField(blank=True),
        full_description=models.TextField(blank=True)
    )

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or self.sku

    @property
    def main_image(self):
        main_img = self.images.filter(is_main=True).first() or self.images.first()
        if main_img:
            return main_img
        variant_img = VariantImage.objects.filter(variant__product=self, is_main=True).first() or VariantImage.objects.filter(variant__product=self).first()
        return variant_img

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    weight = models.CharField(max_length=50, help_text="e.g., 5g, 10g")
    packaging_type = models.CharField(max_length=100, help_text="e.g., Khatam, Crystal")
    base_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Price in base currency, e.g., USD")
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.safe_translation_getter('name', any_language=True)} - {self.weight} {self.packaging_type}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_path)
    alt_text = models.CharField(max_length=255, blank=True, help_text="متن جایگزین برای سئو")
    is_main = models.BooleanField(default=False, help_text="آیا این عکس اصلی است؟")

    def __str__(self):
        return f"Image for {self.product.safe_translation_getter('name', any_language=True)}"

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.endswith('.webp'):
            self.image = optimize_image(self.image)
        super().save(*args, **kwargs)

class VariantImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=variant_image_path)
    alt_text = models.CharField(max_length=255, blank=True, help_text="متن جایگزین برای سئو")
    is_main = models.BooleanField(default=False, help_text="آیا این عکس اصلی متغیر است؟")

    def __str__(self):
        return f"Image for {self.variant}"

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.endswith('.webp'):
            self.image = optimize_image(self.image)
        super().save(*args, **kwargs)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(max_length=100, verbose_name="Email Address")
    subject = models.CharField(max_length=100, verbose_name="Subject")
    message = models.TextField(max_length=5000, verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
