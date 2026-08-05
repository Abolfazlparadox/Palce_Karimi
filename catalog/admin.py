import csv
from django.http import HttpResponse
from django.contrib import admin
from django.utils import timezone
from parler.admin import TranslatableAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from catalog.models import (
    Category, QualityGrade, PackagingType,
    Product, ProductVariant, TieredPrice, ProductImage, ContactMessage, ExchangeRate,NewsletterSubscriber
)

# ==========================================
# Inlines (با نام‌های کاربرپسند)
# ==========================================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = "تصویر محصول"
    verbose_name_plural = "گالری تصاویر محصول"
    readonly_fields = ('image_preview', 'created_at')
    fields = ('image', 'image_preview', 'alt_text', 'order', 'is_main')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px; border-radius:5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);"/>', obj.image.url)
        return "بدون تصویر"
    image_preview.short_description = "پیش‌نمایش"


class ProductVariantInline(admin.StackedInline):
    model = ProductVariant
    extra = 1
    verbose_name = "بسته‌بندی و وزن (متغیر)"
    verbose_name_plural = "انواع بسته‌بندی‌های این محصول"
    fields = ('packaging_type', 'sku', 'weight_in_grams', 'moq', 'is_default')


# ==========================================
# Actions
# ==========================================
@admin.action(description="انتشار و نمایش محصولات انتخاب شده در سایت")
def make_published(modeladmin, request, queryset):
    queryset.update(is_active=True, published_at=timezone.now())

@admin.action(description="مخفی کردن محصولات انتخاب شده از سایت")
def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_active=False, published_at=None)


# ==========================================
# Model Admins
# ==========================================
@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('name', 'category', 'grade', 'is_active', 'main_image_preview', 'created_at')
    list_filter = ('category', 'grade', 'is_active')
    search_fields = ('translations__name', 'variants__sku')
    list_editable = ('is_active',)
    autocomplete_fields = ('category', 'grade')
    inlines = [ProductImageInline, ProductVariantInline]
    date_hierarchy = 'created_at'
    actions = [make_published, make_unpublished]

    # گروه‌بندی فیلدها برای راحتی کارمند (UX)
    fieldsets = (
        ("اطلاعات متنی (چندزبانه)", {
            'fields': ('name', 'slug', 'short_description', 'full_description'),
            'description': "در این بخش نام و توضیحات محصول را وارد کنید. از طریق تب‌های بالا می‌توانید زبان را تغییر دهید."
        }),
        ("دسته‌بندی و کیفیت", {
            'fields': ('category', 'grade'),
            'description': "گروه محصول و درجه کیفی آن را مشخص کنید."
        }),
        ("سئو و موتورهای جستجو", {
            'fields': ('seo_title', 'meta_description'),
            'classes': ('collapse',), # به صورت پیش‌فرض بسته است تا کاربر را گیج نکند
            'description': "این فیلدها در سایت دیده نمی‌شوند و فقط برای گوگل هستند."
        }),
        ("وضعیت انتشار", {
            'fields': ('is_active', 'published_at'),
        }),
    )

    class Media:
        css = {
            'all': ('css/admin_rtl_fix.css',)
        }
    def main_image_preview(self, obj):
        img = obj.main_image
        if img and img.image:
            return format_html('<img src="{}" style="width:45px; height:45px; object-fit:cover; border-radius:5px;"/>', img.image.url)
        return "-"
    main_image_preview.short_description = "عکس اصلی"


@admin.register(TieredPrice)
class TieredPriceAdmin(admin.ModelAdmin):
    list_display = ('product_variant', 'min_qty', 'max_qty', 'price_usd')
    list_editable = ('price_usd',)
    search_fields = ('product_variant__sku', 'product_variant__product__translations__name')
    list_filter = ('product_variant__product__category',)


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('translations__name',)


@admin.register(QualityGrade)
class QualityGradeAdmin(TranslatableAdmin):
    search_fields = ('translations__name',)


@admin.register(PackagingType)
class PackagingTypeAdmin(TranslatableAdmin):
    search_fields = ('translations__name',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'is_read', 'created_at')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at', 'ip_address', 'user_agent')
    list_filter = ('is_read', 'created_at')


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'rate', 'updated_at')
    list_editable = ('rate',)


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'language', 'is_active', 'created_at')
    list_filter = ('is_active', 'language', 'created_at')
    search_fields = ('email', 'ip_address')
    date_hierarchy = 'created_at'
    list_per_page = 50

    # فیلدهایی که نباید توسط ادمین تغییر کنند
    readonly_fields = ('email', 'ip_address', 'user_agent', 'language', 'created_at', 'updated_at')

    actions = ['make_active', 'make_inactive', 'export_to_csv']

    @admin.action(description=_("Activate selected subscribers"))
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _(f"{updated} subscribers successfully activated."))

    @admin.action(description=_("Deactivate selected subscribers"))
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _(f"{updated} subscribers successfully deactivated."))

    @admin.action(description=_("Export selected to CSV (Mailchimp format)"))
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'

        writer = csv.writer(response)
        # هدرهای استاندارد برای نرم‌افزارهای ایمیل مارکتینگ
        writer.writerow(['Email Address', 'Language', 'IP Address', 'Status', 'Date Added'])

        for obj in queryset:
            status = 'Subscribed' if obj.is_active else 'Unsubscribed'
            writer.writerow(
                [obj.email, obj.language, obj.ip_address, status, obj.created_at.strftime("%Y-%m-%d %H:%M:%S")])

        return response