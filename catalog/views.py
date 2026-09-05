import logging

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit
from email_validator import EmailNotValidError, validate_email

from catalog.forms import ContactMessageForm
from catalog.models import (
    Category,
    NewsletterSubscriber,
    Product,
    ProductImage,
    ProductVariant,
    TieredPrice,
)


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Reusable prefetch sets — avoid repeating these strings across views
# ---------------------------------------------------------------------------

_PRODUCT_LIST_PREFETCH = Prefetch(
    "images",
    queryset=ProductImage.objects.filter(is_main=True),
    to_attr="main_image_obj",
)

_PRODUCT_LIST_PREFETCH_FULL = Prefetch(
    "images",
    queryset=ProductImage.objects.order_by("order", "-created_at"),
)

_VARIANT_WITH_PRICES = Prefetch(
    "variants",
    queryset=ProductVariant.objects.prefetch_related(
        Prefetch(
            "tiered_prices",
            queryset=TieredPrice.objects.order_by("min_qty"),
        )
    ).select_related("packaging_type"),
)

_VARIANT_LIGHT = Prefetch(
    "variants",
    queryset=ProductVariant.objects.select_related("packaging_type").only(
        "id", "product_id", "packaging_type_id", "sku",
        "weight_in_grams", "moq", "is_default",
    ),
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_client_ip(request):
    """
    Extract the real client IP.

    X-Forwarded-For is trusted ONLY when SECURE_PROXY_SSL_HEADER or
    a trusted proxy is configured (see settings.SECURE_PROXY_SSL_HEADER).
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------

def home_page(request):
    """Landing page — active categories + 4 latest products."""
    categories = (
        Category.objects
        .filter(is_active=True)
        .prefetch_related("translations")
        .order_by("-created_at")
    )

    latest_products = (
        Product.objects
        .filter(is_active=True)
        .select_related("category", "grade")
        .prefetch_related(
            "translations",
            _PRODUCT_LIST_PREFETCH,
            _VARIANT_LIGHT,
        )
        .order_by("-created_at")[:4]
    )

    context = {
        "categories": categories,
        "latest_products": latest_products,
    }
    return render(request, "index.html", context)


def about_us(request):
    return render(request, "catalog/about_us.html")


@ratelimit(key="ip", rate="5/h", method="POST", block=False)
def contact_us(request):
    if request.method == "POST":
        if getattr(request, "limited", False):
            logger.warning(
                "Rate-limited contact attempt from IP %s",
                get_client_ip(request),
            )
            messages.error(request, _("You have sent too many messages. Please try again later."))
            return redirect("catalog:contact_us")

        form = ContactMessageForm(request.POST)

        if form.is_valid():
            msg = form.save(commit=False)
            msg.ip_address = get_client_ip(request)
            msg.user_agent = request.META.get("HTTP_USER_AGENT", "")[:1000]
            msg.save()

            logger.info("Contact message received successfully.")
            messages.success(request, _("Your message has been sent successfully. We will contact you soon."))
            return redirect("catalog:contact_us")

    else:
        form = ContactMessageForm()

    return render(request, "catalog/contact_us.html", {"form": form})


def shop_page(request):
    """Paginated product catalog."""
    product_list = (
        Product.objects
        .filter(is_active=True)
        .select_related("category", "grade")
        .prefetch_related(
            "translations",
            _PRODUCT_LIST_PREFETCH,
            _VARIANT_LIGHT,
        )
        .order_by("-created_at")
    )

    paginator = Paginator(product_list, 8)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.page(1)

    return render(request, "catalog/shop.html", {"page_obj": page_obj})


def terms_faq(request):
    return render(request, "catalog/terms.html")


def product_detail(request, slug):
    """Single product page — full variant pricing + related products."""
    product = get_object_or_404(
        Product.objects
        .filter(is_active=True)
        .select_related("category", "grade")
        .prefetch_related(
            "translations",
            _PRODUCT_LIST_PREFETCH_FULL,
            _VARIANT_WITH_PRICES,
        ),
        translations__slug=slug,
    )

    related_products = (
        Product.objects
        .filter(category=product.category, is_active=True)
        .exclude(pk=product.pk)
        .select_related("category")
        .prefetch_related(
            "translations",
            _PRODUCT_LIST_PREFETCH,
            _VARIANT_LIGHT,
        )[:4]
    )

    context = {
        "product": product,
        "related_products": related_products,
    }
    return render(request, "catalog/product_detail.html", context)


def category_detail(request, slug):
    """Products filtered by category."""
    category = get_object_or_404(
        Category.objects.filter(is_active=True).prefetch_related("translations"),
        translations__slug=slug,
    )

    product_list = (
        Product.objects
        .filter(category=category, is_active=True)
        .select_related("category", "grade")
        .prefetch_related(
            "translations",
            _PRODUCT_LIST_PREFETCH,
            _VARIANT_LIGHT,
        )
        .order_by("-created_at")
    )

    paginator = Paginator(product_list, 8)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        page_obj = paginator.page(1)

    context = {
        "category": category,
        "page_obj": page_obj,
    }
    return render(request, "catalog/category_detail.html", context)


@require_POST
@ratelimit(key="ip", rate="3/m", method="POST", block=False)
def newsletter_subscribe(request):
    if getattr(request, "limited", False):
        logger.warning("Rate-limited newsletter attempt from IP %s", get_client_ip(request))
        messages.error(request, _("Too many requests. Please try again later."))
        return redirect("catalog:home")

    raw_email = request.POST.get("newsletterEmail", "")
    email = raw_email.strip().lower()

    if not email:
        messages.error(request, _("Please enter an email address."))
        return redirect("catalog:home")

    try:
        valid_email_obj = validate_email(email, check_deliverability=True)
        normalized_email = valid_email_obj.normalized

        user_ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:1000]
        user_lang = request.LANGUAGE_CODE

        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=normalized_email,
            defaults={
                "ip_address": user_ip,
                "user_agent": user_agent,
                "language": user_lang,
            },
        )

        if created:
            logger.info("New newsletter subscription: %s", normalized_email)
            messages.success(request, _("Thank you for subscribing to our newsletter."))
        else:
            messages.info(request, _("You are already subscribed to our email list."))

    except EmailNotValidError as exc:
        logger.warning(
            "Invalid newsletter attempt: %s — Reason: %s",
            email,
            str(exc),
        )
        messages.error(request, _("Invalid email address. Please check and try again."))

    safe_redirect = _safe_redirect(request)
    return redirect(safe_redirect)


# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------

def _safe_redirect(request):
    """Return a safe redirect URL (referer or home fallback)."""
    referer = request.META.get("HTTP_REFERER")
    if referer and url_has_allowed_host_and_scheme(
        referer,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return referer
    return "catalog:home"