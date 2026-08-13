import os
import uuid
from decimal import Decimal
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from parler.models import TranslatableModel, TranslatedFields
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _

# ==========================================
# 0. Utility Functions
# ==========================================
def get_image_upload_path(instance, filename):
    # تغییر هوشمندانه: پسوند را همیشه روی webp قفل می‌کنیم
    new_filename = f"{uuid.uuid4().hex}.webp"
    return os.path.join('products', str(instance.product.uuid), new_filename)
# ==========================================
# 1. Base / Taxonomy Models
# ==========================================

class Category(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(verbose_name="نام دسته‌بندی", max_length=200),
        slug=models.SlugField(verbose_name="شناسه (Slug)", max_length=220, unique=True, allow_unicode=True),
        description=models.TextField(verbose_name="توضیحات", blank=True)
    )
    is_active = models.BooleanField(verbose_name="وضعیت فعالیت", default=True, db_index=True)
    created_at = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name="تاریخ بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'دسته‌بندی بدون ترجمه'


class QualityGrade(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(verbose_name="درجه کیفی", max_length=100)
    )
    created_at = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="تاریخ بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "درجه کیفی"
        verbose_name_plural = "درجات کیفی"

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'درجه کیفی بدون ترجمه'


class PackagingType(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(verbose_name="نوع بسته‌بندی", max_length=100)
    )
    created_at = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="تاریخ بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "نوع بسته‌بندی"
        verbose_name_plural = "انواع بسته‌بندی"

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'بسته‌بندی بدون ترجمه'


# ==========================================
# 2. Core Product Architecture (B2B)
# ==========================================

class Product(TranslatableModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    translations = TranslatedFields(
        name=models.CharField(verbose_name="نام محصول", max_length=200),
        slug=models.SlugField(verbose_name="شناسه URL (اسلاگ)", max_length=220, unique=True, allow_unicode=True),
        short_description=models.CharField(verbose_name="توضیح کوتاه", max_length=500),
        full_description=models.TextField(verbose_name="توضیحات کامل"),
        seo_title=models.CharField(verbose_name="عنوان سئو", max_length=255, blank=True),
        meta_description=models.CharField(verbose_name="توضیحات متا (SEO)", max_length=300, blank=True)
    )

    category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT, verbose_name="دسته‌بندی محصول")
    grade = models.ForeignKey(QualityGrade, related_name='products', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="درجه کیفی")

    is_active = models.BooleanField(verbose_name="نمایش در سایت", default=True, db_index=True)
    published_at = models.DateTimeField(verbose_name="تاریخ انتشار", null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(verbose_name="تاریخ بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        ordering = ['-created_at']

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or 'محصول بدون ترجمه'

    @property
    def default_variant(self):
        variant = self.variants.filter(is_default=True).first()
        return variant if variant else self.variants.first()

    @property
    def main_image(self):
        # Use prefetched result when available (avoids N+1 queries)
        if hasattr(self, 'main_image_obj'):
            return self.main_image_obj[0] if self.main_image_obj else None
        img = self.images.filter(is_main=True).first()
        return img if img else self.images.order_by('order').first()


class ProductVariant(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE, verbose_name="محصول مرتبط")
    packaging_type = models.ForeignKey(PackagingType, related_name='variants', on_delete=models.PROTECT, verbose_name="نوع بسته‌بندی")

    sku = models.CharField(verbose_name="کد کالا (SKU)", max_length=100, unique=True, db_index=True)
    weight_in_grams = models.DecimalField(verbose_name="وزن (گرم)" ,decimal_places=2,max_digits=100)
    moq = models.PositiveIntegerField(verbose_name="حداقل سفارش (MOQ)", default=1)
    is_default = models.BooleanField(verbose_name="متغیر پیش‌فرض", default=False, help_text="این متغیر به عنوان قیمت و ویژگی اصلی محصول نمایش داده می‌شود.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "متغیر محصول"
        verbose_name_plural = "متغیرهای محصول"
        ordering = ['weight_in_grams']
        constraints = [
            models.UniqueConstraint(fields=["product", "packaging_type", "weight_in_grams"], name="unique_product_variant"),
            models.UniqueConstraint(fields=["product"], condition=Q(is_default=True), name="unique_default_variant_per_product")
        ]
    @property
    def base_price(self):
        """بازگرداندن قیمت پایه (اولین رنج قیمت) به دلار"""
        first_tier = self.tiered_prices.order_by('min_qty').first()
        if first_tier:
            return first_tier.price_usd
        return Decimal('0.00')

    def __str__(self):
        pkg_name = self.packaging_type.safe_translation_getter('name', any_language=True) or 'Pkg'
        return f"{self.product} - {self.weight_in_grams}g ({pkg_name})"


# ==========================================
# 3. Product Details (Prices & Images)
# ==========================================

class TieredPrice(models.Model):
    product_variant = models.ForeignKey(ProductVariant, related_name='tiered_prices', on_delete=models.CASCADE, verbose_name="متغیر محصول")
    min_qty = models.PositiveIntegerField(verbose_name="حداقل تعداد")
    max_qty = models.PositiveIntegerField(verbose_name="حداکثر تعداد", null=True, blank=True)
    price_usd = models.DecimalField(verbose_name="قیمت (دلار)", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "قیمت پلکانی"
        verbose_name_plural = "قیمت‌های پلکانی"
        ordering = ['min_qty']

    def clean(self):
        super().clean()
        if self.max_qty is not None and self.min_qty >= self.max_qty:
            raise ValidationError({'max_qty': "حداکثر تعداد باید بزرگتر از حداقل تعداد باشد."})

        def overlaps(a_min, a_max, b_min, b_max):
            if a_max is None and b_max is None: return True
            if a_max is None: return b_max is None or b_max >= a_min
            if b_max is None: return a_max >= b_min
            return a_min <= b_max and b_min <= a_max

        existing = TieredPrice.objects.filter(product_variant=self.product_variant).exclude(pk=self.pk)
        for tier in existing:
            if overlaps(self.min_qty, self.max_qty, tier.min_qty, tier.max_qty):
                raise ValidationError("بازه قیمت‌ها با هم تداخل دارند.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.max_qty:
            return f"{self.min_qty} تا {self.max_qty} عدد: ${self.price_usd}"
        return f"{self.min_qty} عدد به بالا: ${self.price_usd}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, verbose_name="محصول")
    image = ResizedImageField(
        size=[300, 400],  # ابعاد هدف (۳۰۰ عرض، ۴۰۰ ارتفاع)
        crop=['middle', 'center'],  # برش هوشمند از مرکز
        quality=85,  # کیفیت بهینه برای حفظ وضوح و کاهش حجم
        force_format='WEBP',  # اجبار به فرمت نسل جدید
        verbose_name="تصویر",
        upload_to=get_image_upload_path
    )
    alt_text = models.CharField(verbose_name="متن جایگزین (Alt)", max_length=255, blank=True)
    order = models.PositiveIntegerField(verbose_name="ترتیب نمایش", default=0)
    is_main = models.BooleanField(verbose_name="تصویر اصلی است؟", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"
        ordering = ["order", "-created_at"]

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"تصویر {self.order} برای {self.product}"


# ==========================================
# 4. Operations & External Models
# ==========================================

class ContactMessage(models.Model):
    name = models.CharField(verbose_name="نام و نام خانوادگی", max_length=100)
    email = models.EmailField(verbose_name="ایمیل", max_length=100)
    subject = models.CharField(verbose_name="موضوع پیام", max_length=100)
    message = models.TextField(verbose_name="متن پیام", max_length=5000)

    is_read = models.BooleanField(verbose_name="خوانده شده؟", default=False, db_index=True)
    ip_address = models.GenericIPAddressField(verbose_name="آی‌پی کاربر", null=True, blank=True)
    user_agent = models.TextField(verbose_name="مرورگر کاربر", blank=True)

    created_at = models.DateTimeField(verbose_name="تاریخ ثبت", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "پیام ارتباط با ما"
        verbose_name_plural = "پیام‌های کاربران"
        ordering = ['-created_at']

    def __str__(self):
        status = "خوانده شده" if self.is_read else "جدید"
        return f"[{status}] {self.name} - {self.subject}"


class ExchangeRate(models.Model):
    class Currency(models.TextChoices):
        USD = 'USD', 'دلار آمریکا'
        EUR = 'EUR', 'یورو'
        AED = 'AED', 'درهم امارات'
        TRY = 'TRY', 'لیر ترکیه'
        IRR = 'IRR', 'ریال ایران'

    currency = models.CharField(
        verbose_name="کد ارز",
        max_length=5,
        choices=Currency.choices,
        unique=True
    )
    rate = models.DecimalField(verbose_name="نرخ تبدیل", max_digits=15, decimal_places=4)
    updated_at = models.DateTimeField(verbose_name="آخرین بروزرسانی", auto_now=True)

    class Meta:
        verbose_name = "نرخ ارز"
        verbose_name_plural = "نرخ‌های ارز"
        ordering = ['currency']

    def __str__(self):
        return f"{self.get_currency_display()} - {self.rate}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(
        _("Email Address"),
        unique=True,
        db_index=True
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True
    )
    language = models.CharField(
        _("Language"),
        max_length=10,
        blank=True
    )
    ip_address = models.GenericIPAddressField(
        _("IP Address"),
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        _("User Agent"),
        blank=True
    )
    created_at = models.DateTimeField(
        _("Subscribed At"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = _("مشترک خبرنامه")
        verbose_name_plural = _("مشترکین خبرنامه")
        ordering = ['-created_at']

    def __str__(self):
        return self.email
