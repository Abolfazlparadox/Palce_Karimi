import csv

from django.http import HttpResponse
from django.contrib import admin
from django.utils import timezone
from django.db.models import Count
from parler.admin import TranslatableAdmin
from django.utils.html import format_html
from django.urls import reverse, NoReverseMatch
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from catalog.models import (
    Category, QualityGrade, PackagingType,
    Product, ProductVariant, TieredPrice, ProductImage, ContactMessage,
    ExchangeRate, NewsletterSubscriber,
)

# =============================================================================
# Site Branding
# =============================================================================
admin.site.site_header = "پالاس کریمی — مدیریت صادرات"
admin.site.site_title = "پالاس کریمی | پنل مدیریت"
admin.site.index_title = "به مدیریت پالاس کریمی خوش آمدید"


# =============================================================================
# Mixins — Shared Helpers
# =============================================================================
class StatusBadgeMixin:
    """Reusable pill-style badge renderer."""

    @staticmethod
    def _badge(text, bg_color, text_color, border_color=None):
        border = f'border:1px solid {border_color};' if border_color else ''
        return format_html(
            '<span style="display:inline-block;background:{};color:{};'
            'font-weight:600;padding:3px 10px;border-radius:12px;font-size:12px;'
            'white-space:nowrap;{}">{}</span>',
            bg_color, text_color, border, text
        )


# =============================================================================
# RTL-Aware Media Injection (Language-based)
# =============================================================================
class RTLAdminMediaMixin:
    """
    Inject admin CSS/JS conditionally.

    The rtl.css and admin_custom.js are loaded via
    admin/base_site.html (template override), NOT from individual ModelAdmin
    Media classes. This prevents RTL styles from breaking LTR languages.

    See: templates/admin/base_site.html for the template implementation.
    """


# =============================================================================
# Inlines — Product Images (Gallery-Style Tabular)
# =============================================================================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = _("تصویر")
    verbose_name_plural = _("گالری محصول")
    readonly_fields = ('image_preview', 'created_at')
    fields = ('image', 'image_preview', 'is_main', 'order', 'alt_text', 'created_at')
    ordering = ('order', '-created_at')

    def image_preview(self, obj):
        if obj.image:
            border = '#C5A059' if obj.is_main else '#3A4F6F'
            # اسپن ستاره را فقط برای تصویر اصلی می‌سازیم
            if obj.is_main:
                star_span = (
                    ''
                )
            else:
                star_span = ''
            return format_html(
                '<div style="position:relative;width:60px;height:60px;">'
                '<img src="{}" style="width:60px;height:60px;object-fit:cover;'
                'border-radius:6px;border:2px solid {};box-shadow:0 2px 6px rgba(0,0,0,.12);"/>'
                '{}</div>',
                obj.image.url, border, star_span
            )
            return mark_safe(
                '<span style="color:#8899AA;font-size:11px;font-style:italic;">بدون تصویر</span>'
            )

    image_preview.short_description = _("پیش‌نمایش")


# =============================================================================
# Inlines — Product Variants (Compact Table)
# =============================================================================
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    verbose_name = _("گونه")
    verbose_name_plural = _("گونه‌های محصول")
    fields = ('packaging_type', 'sku', 'weight_in_grams', 'moq', 'is_default', 'base_price_display')
    readonly_fields = ('base_price_display',)
    ordering = ('weight_in_grams',)

    def base_price_display(self, obj):
        if obj.pk:
            price = obj.base_price
            return format_html(
                '<span style="color:#C5A059;font-weight:700;font-size:13px;">${}</span>',
                price
            )
            return mark_safe(
                '<span style="color:#8899AA;font-size:11px;">—</span>'
            )
    base_price_display.short_description = _("قیمت پایه")


# =============================================================================
# Custom Actions
# =============================================================================
@admin.action(description=_("انتشار محصولات انتخاب‌شده"))
def make_published(modeladmin, request, queryset):
    updated = queryset.update(is_active=True, published_at=timezone.now())
    modeladmin.message_user(request, _("%(count)d محصول با موفقیت منتشر شد.") % {'count': updated})


@admin.action(description=_("عدم انتشار محصولات انتخاب‌شده"))
def make_unpublished(modeladmin, request, queryset):
    updated = queryset.update(is_active=False, published_at=None)
    modeladmin.message_user(request, _("%(count)d محصول از حالت انتشار خارج شد.") % {'count': updated})


@admin.action(description=_("علامت‌گذاری پیام‌های انتخاب‌شده به عنوان خوانده‌شده"))
def mark_as_read(modeladmin, request, queryset):
    updated = queryset.update(is_read=True)
    modeladmin.message_user(request, _("%(count)d پیام به عنوان خوانده‌شده علامت‌گذاری شد.") % {'count': updated})


@admin.action(description=_("علامت‌گذاری پیام‌های انتخاب‌شده به عنوان خوانده‌نشده"))
def mark_as_unread(modeladmin, request, queryset):
    updated = queryset.update(is_read=False)
    modeladmin.message_user(request, _("%(count)d پیام به عنوان خوانده‌نشده علامت‌گذاری شد.") % {'count': updated})


@admin.action(description=_("فعال‌سازی مشترکین انتخاب‌شده"))
def make_active(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, _("%(count)d مشترک فعال شد.") % {'count': updated})


@admin.action(description=_("غیرفعال‌سازی مشترکین انتخاب‌شده"))
def make_inactive(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, _("%(count)d مشترک غیرفعال شد.") % {'count': updated})


@admin.action(description=_("خروجی CSV از مشترکین انتخاب‌شده"))
def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="palace_karimi_subscribers.csv"'
    writer = csv.writer(response)
    writer.writerow(['ایمیل', 'زبان', 'آدرس IP', 'وضعیت', 'تاریخ اشتراک'])
    for obj in queryset:
        status = 'فعال' if obj.is_active else 'لغو اشتراک'
        writer.writerow([
            obj.email, obj.language, obj.ip_address or '',
            status, obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
        ])
    return response


# =============================================================================
# Product Admin
# =============================================================================
@admin.register(Product)
class ProductAdmin(TranslatableAdmin, StatusBadgeMixin, RTLAdminMediaMixin):
    delete_confirmation_max_display = None
    list_display = (
        'main_image_thumb', 'name', 'category', 'grade',
        'status_badge', 'variant_count', 'created_at'
    )
    list_filter = ('category', 'grade', 'is_active', 'created_at')
    search_fields = ('translations__name', 'translations__slug', 'variants__sku')
    list_select_related = ('category', 'grade')
    autocomplete_fields = ('category', 'grade')
    inlines = [ProductImageInline, ProductVariantInline]
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    actions = [make_published, make_unpublished]
    list_per_page = 25
    show_full_result_count = False

    fieldsets = (
        (_("اطلاعات محصول (چندزبانه)"), {
            'fields': ('name', 'slug', 'short_description', 'full_description'),
            'description': _(
                "جزئیات محصول را وارد کنید. از زبانه‌های زبان برای مدیریت ترجمه‌ها "
                "به فارسی، انگلیسی، عربی و ترکی استفاده کنید."
            ),
        }),
        (_("طبقه‌بندی B2B"), {
            'fields': ('category', 'grade'),
            'description': _(
                "محصول را به یک دسته‌بندی و در صورت نیاز به یک درجه کیفیت اختصاص دهید."
            ),
        }),
        (_("سئو"), {
            'fields': ('seo_title', 'meta_description'),
            'classes': ('collapse', 'pk-collapsible'),
            'description': _(
                "ظاهر صفحه محصول را در نتایج جستجو بهینه کنید. "
                "برای تولید خودکار از نام محصول، خالی بگذارید."
            ),
        }),
        (_("وضعیت انتشار"), {
            'fields': ('is_active', 'published_at'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related(
            'translations', 'images', 'variants__tiered_prices',
            'variants__packaging_type__translations'
        )

    def main_image_thumb(self, obj):
        img = obj.main_image
        if img and img.image:
            return format_html(
                '<img src="{}" style="width:44px;height:44px;object-fit:cover;'
                'border-radius:8px;border:2px solid #C5A059;'
                'box-shadow:0 1px 4px rgba(0,0,0,.15);"/>',
                img.image.url
            )
        return mark_safe(
            '<div style="width:44px;height:44px;border-radius:8px;'
            'border:2px dashed #3A4F6F;display:flex;align-items:center;'
            'justify-content:center;color:#6B7C8A;font-size:16px;">'
            '&#128444;</div>'
        )
    main_image_thumb.short_description = _("تصویر")

    def status_badge(self, obj):
        if obj.is_active:
            return self._badge(_("منتشر شده"), '#E8F5E3', '#2E7D32', '#A5D6A7')
        return self._badge(_("پیش‌نویس"), '#FFF3E0', '#E65100', '#FFCC80')
    status_badge.short_description = _("وضعیت")

    def variant_count(self, obj):
        count = obj.variants.count()
        color = '#C5A059' if count > 0 else '#8899AA'
        return format_html(
            '<span style="color:{};font-weight:600;">{}</span>',
            color, count
        )
    variant_count.short_description = _("گونه‌ها")

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

# =============================================================================
# TieredPrice Admin
# =============================================================================
@admin.register(TieredPrice)
class TieredPriceAdmin(admin.ModelAdmin, RTLAdminMediaMixin):
    list_display = (
        'product_link', 'variant_sku', 'tier_range', 'price_display'
    )
    list_filter = ('product_variant__product__category',)
    search_fields = (
        'product_variant__sku',
        'product_variant__product__translations__name',
    )
    ordering = ('product_variant__product', 'product_variant', 'min_qty')

    fieldsets = (
        (_("جزئیات قیمت‌گذاری"), {
            'fields': ('product_variant', 'min_qty', 'max_qty', 'price_usd'),
            'description': _(
                "قیمت‌گذاری بر اساس مقدار را برای این گونه تعریف کنید. "
                "برای بالاترین سطح (مثلاً ۱۰۰+)، حداکثر تعداد را خالی بگذارید."
            ),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'product_variant__product',
            'product_variant__packaging_type',
        ).prefetch_related('product_variant__product__translations')

    def product_link(self, obj):
        product = obj.product_variant.product
        name = product.safe_translation_getter('name', any_language=True) or str(product)
        try:
            url = reverse('admin:catalog_product_change', args=[product.pk])
            return format_html(
                '<a href="{}" style="color:#C5A059;font-weight:600;">{}</a>',
                url, name
            )
        except NoReverseMatch:
            return format_html('<span style="font-weight:600;">{}</span>', name)
    product_link.short_description = _("محصول")

    def variant_sku(self, obj):
        return format_html(
            '<code style="background:#1A2942;color:#E8E2D8;padding:2px 8px;'
            'border-radius:4px;font-size:12px;">{}</code>',
            obj.product_variant.sku
        )
    variant_sku.short_description = _("کد انبار")

    def tier_range(self, obj):
        if obj.max_qty:
            return format_html(
                '<span style="font-weight:600;">'
                '<span style="color:#8899AA;">{}</span>'
                ' &mdash; '
                '<span style="color:#8899AA;">{}</span></span>',
                obj.min_qty, obj.max_qty
            )
        return format_html(
            '<span style="font-weight:600;">'
            '<span style="color:#8899AA;">{}</span>+</span>',
            obj.min_qty
        )
    tier_range.short_description = _("بازه تعداد")

    def price_display(self, obj):
        return format_html(
            '<span style="color:#C5A059;font-weight:700;font-size:14px;">${}</span>',
            obj.price_usd
        )
    price_display.short_description = _("قیمت (دلار)")


# =============================================================================
# Category Admin
# =============================================================================
@admin.register(Category)
class CategoryAdmin(TranslatableAdmin, StatusBadgeMixin, RTLAdminMediaMixin):
    list_display = ('name', 'slug', 'product_count', 'status_badge')
    list_filter = ('is_active',)
    search_fields = ('translations__name', 'translations__slug')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_product_count=Count('products'))

    def product_count(self, obj):
        count = getattr(obj, '_product_count', None) or obj.products.count()
        return format_html(
            '<span style="font-weight:600;color:#C5A059;">{}</span>', count
        )
    product_count.short_description = _("محصولات")

    def status_badge(self, obj):
        if obj.is_active:
            return self._badge(_("فعال"), '#E8F5E3', '#2E7D32', '#A5D6A7')
        return self._badge(_("غیرفعال"), '#FFF3E0', '#E65100', '#FFCC80')
    status_badge.short_description = _("وضعیت")

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

# =============================================================================
# QualityGrade Admin
# =============================================================================
@admin.register(QualityGrade)
class QualityGradeAdmin(TranslatableAdmin, RTLAdminMediaMixin):
    list_display = ('name', 'product_count')
    search_fields = ('translations__name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_product_count=Count('products'))

    def product_count(self, obj):
        count = getattr(obj, '_product_count', None) or obj.products.count()
        return format_html(
            '<span style="font-weight:600;color:#C5A059;">{}</span>', count
        )
    product_count.short_description = _("محصولات")


# =============================================================================
# PackagingType Admin
# =============================================================================
@admin.register(PackagingType)
class PackagingTypeAdmin(TranslatableAdmin, RTLAdminMediaMixin):
    list_display = ('name', 'variant_count')
    search_fields = ('translations__name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_variant_count=Count('variants'))

    def variant_count(self, obj):
        count = getattr(obj, '_variant_count', None) or obj.variants.count()
        return format_html(
            '<span style="font-weight:600;color:#C5A059;">{}</span>', count
        )
    variant_count.short_description = _("گونه‌ها")


# =============================================================================
# ContactMessage Admin
# =============================================================================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin, StatusBadgeMixin, RTLAdminMediaMixin):
    list_display = (
        'read_status_badge', 'sender_name', 'subject_preview',
        'sender_email', 'created_at'
    )
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = (
        'name', 'email', 'subject', 'message',
        'created_at', 'ip_address', 'user_agent', 'is_read'
    )
    actions = [mark_as_read, mark_as_unread]
    ordering = ('-created_at',)
    list_per_page = 30
    date_hierarchy = 'created_at'

    fieldsets = (
        (_("محتوای پیام"), {
            'fields': ('subject', 'message'),
            'classes': ('pk-wide-field',),
        }),
        (_("اطلاعات فرستنده"), {
            'fields': ('name', 'email', 'created_at', 'ip_address'),
            'classes': ('pk-inline-row',),
        }),
        (_("جزئیات فنی"), {
            'fields': ('user_agent', 'is_read'),
            'classes': ('collapse',),
        }),
    )

    def read_status_badge(self, obj):
        if obj.is_read:
            return self._badge(_("خوانده‌شده"), '#E8F5E3', '#2E7D32', '#A5D6A7')
        return self._badge(_("جدید"), '#FFF8E1', '#F57F17', '#FFE082')
    read_status_badge.short_description = _("وضعیت")

    def sender_name(self, obj):
        weight = '400' if obj.is_read else '700'
        color = '#8899AA' if obj.is_read else '#E8E2D8'
        return format_html(
            '<span style="font-weight:{};color:{};">{}</span>',
            weight, color, obj.name
        )
    sender_name.short_description = _("فرستنده")
    sender_name.admin_order_field = 'name'

    def subject_preview(self, obj):
        weight = '400' if obj.is_read else '600'
        color = '#8899AA' if obj.is_read else '#E8E2D8'
        subject = obj.subject[:60] + ('...' if len(obj.subject) > 60 else '')
        return format_html(
            '<span style="font-weight:{};color:{};">{}</span>',
            weight, color, subject
        )
    subject_preview.short_description = _("موضوع")
    subject_preview.admin_order_field = 'subject'

    def sender_email(self, obj):
        return format_html(
            '<span style="color:#6B7C8A;font-size:12px;">{}</span>',
            obj.email
        )
    sender_email.short_description = _("ایمیل")
    sender_email.admin_order_field = 'email'


# =============================================================================
# ExchangeRate Admin
# =============================================================================
@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin, RTLAdminMediaMixin):
    list_display = ('currency_flag', 'currency_name', 'rate', 'updated_at')
    list_editable = ('rate',)
    ordering = ('currency',)

    CURRENCY_META = {
        'USD': {'flag': '🇺🇸', 'name': 'دلار آمریکا'},
        'EUR': {'flag': '🇪🇺', 'name': 'یورو'},
        'AED': {'flag': '🇦🇪', 'name': 'درهم امارات'},
        'TRY': {'flag': '🇹🇷', 'name': 'لیر ترکیه'},
        'IRR': {'flag': '🇮🇷', 'name': 'ریال ایران'},
    }

    def currency_flag(self, obj):
        meta = self.CURRENCY_META.get(obj.currency, {})
        return format_html(
            '<span style="font-size:20px;line-height:1;">{}</span>',
            meta.get('flag', '💱')
        )
    currency_flag.short_description = ""

    def currency_name(self, obj):
        meta = self.CURRENCY_META.get(obj.currency, {})
        return format_html(
            '<div>'
            '<span style="font-weight:700;color:#E8E2D8;">{}</span>'
            '<br><span style="color:#8899AA;font-size:11px;">{}</span>'
            '</div>',
            meta.get('name', obj.get_currency_display()), obj.currency
        )
    currency_name.short_description = _("ارز")

    def rate_display(self, obj):
        return format_html(
            '<span style="color:#C5A059;font-weight:700;font-size:15px;'
            'font-variant-numeric:tabular-nums;">{:,}</span>',
            obj.rate
        )
    rate_display.short_description = _("نرخ")


# =============================================================================
# NewsletterSubscriber Admin
# =============================================================================
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin, StatusBadgeMixin, RTLAdminMediaMixin):
    list_display = ('email', 'language_display', 'status_badge', 'created_at')
    list_filter = ('is_active', 'language', 'created_at')
    search_fields = ('email', 'ip_address')
    date_hierarchy = 'created_at'
    list_per_page = 50
    show_full_result_count = False
    readonly_fields = ('email', 'ip_address', 'user_agent', 'language', 'created_at', 'updated_at')
    actions = [make_active, make_inactive, export_to_csv]
    ordering = ('-created_at',)

    def status_badge(self, obj):
        if obj.is_active:
            return self._badge(_("فعال"), '#E8F5E3', '#2E7D32', '#A5D6A7')
        return self._badge(_("لغو اشتراک"), '#FFEBEE', '#C62828', '#EF9A9A')
    status_badge.short_description = _("وضعیت")

    def language_display(self, obj):
        lang_map = {
            'fa': 'فارسی',
            'en': 'انگلیسی',
            'ar': 'عربی',
            'tr': 'ترکی',
        }
        display = lang_map.get(obj.language, obj.language.upper() if obj.language else '—')
        return format_html(
            '<span style="font-size:12px;color:#8899AA;">{}</span>', display
        )
    language_display.short_description = _("زبان")
