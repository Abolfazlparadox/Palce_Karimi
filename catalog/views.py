import logging
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from email_validator import validate_email, EmailNotValidError
from django_ratelimit.decorators import ratelimit
from catalog.models import NewsletterSubscriber
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalog.models import Category, Product
from catalog.forms import ContactMessageForm
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.decorators.http import require_GET

logger = logging.getLogger(__name__)
def get_client_ip(request):
    """استخراج IP واقعی کاربر حتی در صورت استفاده از پروکسی یا کلودفلر"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')

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

def shop_page(request):
    product_list = Product.objects.filter(is_active=True).order_by('-created_at')
    paginator = Paginator(product_list, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'catalog/shop.html', {'page_obj': page_obj})

def terms_faq(request):
    """
    Renders the Terms, Conditions & FAQ page.
    """
    return render(request, 'catalog/terms.html')

def product_detail(request, slug):
    """
    Displays the detail page for a single product.
    """
    product = get_object_or_404(
        Product.objects.prefetch_related(
            'translations', 'images', 'variants__tiered_prices', 'category__translations'
        ),
        translations__slug=slug,
        is_active=True
    )
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk).prefetch_related('translations', 'images', 'variants')[:4]

    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'catalog/product_detail.html', context)

def category_detail(request, slug):
    """
    Lists all active products within a specific category, with pagination.
    """
    category = get_object_or_404(Category.objects.prefetch_related('translations'), translations__slug=slug)
    product_list = Product.objects.filter(category=category, is_active=True).order_by('-created_at')
    paginator = Paginator(product_list, 4)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, 'catalog/category_detail.html', context)


@ratelimit(key='ip', rate='3/m', method='POST', block=False)
def newsletter_subscribe(request):
    # بررسی Rate Limit
    if getattr(request, 'limited', False):
        messages.error(request, _("Too many requests. Please try again later."))
        return redirect(request.headers.get("Referer", reverse("catalog:home")))

    if request.method == 'POST':
        raw_email = request.POST.get('newsletterEmail', '')
        # نرمال‌سازی ایمیل
        email = raw_email.strip().lower()

        if email:
            try:
                # اعتبارسنجی دقیق فرمت و دامنه (Domain & MX Records)
                valid_email_obj = validate_email(email, check_deliverability=True)
                normalized_email = valid_email_obj.normalized

                # استخراج اطلاعات مارکتینگ
                user_ip = get_client_ip(request)
                user_agent = request.META.get('HTTP_USER_AGENT', '')
                user_lang = request.LANGUAGE_CODE

                # جلوگیری از Race Condition با get_or_create
                obj, created = NewsletterSubscriber.objects.get_or_create(
                    email=normalized_email,
                    defaults={
                        'ip_address': user_ip,
                        'user_agent': user_agent,
                        'language': user_lang,
                    }
                )

                if created:
                    messages.success(request, _("Thank you for subscribing to our newsletter."))
                else:
                    messages.info(request, _("You are already subscribed to our email list."))

            except EmailNotValidError as e:
                # لاگ کردن خطاهای احتمالی برای بررسی‌های امنیتی
                logger.warning(f"Invalid newsletter attempt: {email} - Reason: {str(e)}")
                messages.error(request, _("Invalid email address. Please check and try again."))
        else:
            messages.error(request, _("Please enter an email address."))

    # هدایت امن کاربر به صفحه‌ای که بوده
    return redirect(request.headers.get("Referer", reverse("catalog:home")))
