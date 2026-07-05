from django.shortcuts import render
from .models import Category, Product

def home_page(request):
    # Fetch active products with their translations to avoid N+1 queries
    products = Product.objects.filter(is_active=True).prefetch_related('translations')
    categories = Category.objects.filter(is_active=True).prefetch_related('translations')
    latest_products = Product.objects.filter(is_active=True).prefetch_related('translations', 'images', 'variants').order_by('-id')[:4]
    
    context = {
        'products': products,
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'index.html', context)