from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category

class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages like 'about us', 'contact us', etc.
    """
    i18n = True
    alternates = True
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        # Return a list of URL names for your static pages
        return ['catalog:home', 'catalog:shop', 'catalog:about_us', 'catalog:terms_faq', 'catalog:contact_us']

    def location(self, item):
        return reverse(item)

class ProductSitemap(Sitemap):
    """
    Sitemap for all active products.
    """
    i18n = True
    alternates = True
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.filter(is_active=True).order_by('-updated_at')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Assuming you have a URL named 'product_detail' that takes a slug
        return reverse('catalog:product_detail', kwargs={'slug': obj.slug})

class CategorySitemap(Sitemap):
    """
    Sitemap for all active categories.
    """
    i18n = True
    alternates = True
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Category.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        # Assuming you have a URL named 'category_detail' that takes a slug
        return reverse('catalog:category_products', kwargs={'slug': obj.slug})
