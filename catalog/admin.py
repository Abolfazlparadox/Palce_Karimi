from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Product, ProductVariant, ProductImage, VariantImage, ExchangeRate, ContactMessage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return "(No Image)"
    image_preview.short_description = 'Image Preview'

class VariantImageInline(admin.TabularInline):
    model = VariantImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        from django.utils.html import format_html
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return "(No Image)"
    image_preview.short_description = 'Image Preview'

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    inlines = [VariantImageInline]

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('translations__name', 'translations__slug')

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ('name', 'sku', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('translations__name', 'sku', 'category__translations__name')
    inlines = [ProductImageInline, ProductVariantInline]
    date_hierarchy = 'created_at'

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'weight', 'packaging_type', 'base_price', 'stock')
    list_filter = ('product__category',)
    search_fields = ('product__translations__name', 'weight', 'packaging_type')
    inlines = [VariantImageInline]

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency_code', 'rate_to_base', 'last_updated')
    readonly_fields = ('last_updated',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)
