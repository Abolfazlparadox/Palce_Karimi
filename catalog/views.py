from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Product
from .forms import ContactMessageForm

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

def about_us(request):
    return render(request, 'catalog/about_us.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'success_contact')
            return redirect('catalog:contact_us')
        else:
            messages.error(request, 'error_contact')
    
    return render(request, 'catalog/contact_us.html')
