import logging
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django_ratelimit.decorators import ratelimit
from email_validator import EmailNotValidError, validate_email
from catalog.forms import ContactMessageForm
from catalog.models import Category, NewsletterSubscriber, Product


logger = logging.getLogger(__name__)


def get_client_ip(request):
    """
    Extract the client IP address.

    X-Forwarded-For should only be trusted when the application is
    behind a trusted reverse proxy that correctly sets/overwrites it.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def home_page(request):
    categories = (
        Category.objects
        .filter(is_active=True)
        .prefetch_related("translations")
    )

    latest_products = (
        Product.objects
        .filter(is_active=True)
        .prefetch_related(
            "translations",
            "images",
            "variants",
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


def contact_us(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, _("success_contact"))
            return redirect("catalog:contact_us")

        messages.error(request, _("error_contact"))

    else:
        form = ContactMessageForm()

    return render(
        request,
        "catalog/contact_us.html",
        {"form": form},
    )


def shop_page(request):
    product_list = (
        Product.objects
        .filter(is_active=True)
        .prefetch_related(
            "translations",
            "images",
            "variants",
        )
        .order_by("-created_at")
    )

    paginator = Paginator(product_list, 4)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "catalog/shop.html",
        {"page_obj": page_obj},
    )


def terms_faq(request):
    return render(request, "catalog/terms.html")


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects
        .select_related(
            "category",
            "grade",
        )
        .prefetch_related(
            "translations",
            "images",
            "variants__tiered_prices",
        ),
        translations__slug=slug,
        is_active=True,
    )

    related_products = (
        Product.objects
        .filter(
            category=product.category,
            is_active=True,
        )
        .exclude(pk=product.pk)
        .select_related("category", "grade")
        .prefetch_related(
            "translations",
            "images",
            "variants",
        )[:4]
    )

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(
        request,
        "catalog/product_detail.html",
        context,
    )


def category_detail(request, slug):
    category = get_object_or_404(
        Category.objects.prefetch_related("translations"),
        translations__slug=slug,
    )

    product_list = (
        Product.objects
        .filter(
            category=category,
            is_active=True,
        )
        .select_related("category", "grade")
        .prefetch_related(
            "translations",
            "images",
            "variants",
        )
        .order_by("-created_at")
    )

    paginator = Paginator(product_list, 4)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "category": category,
        "page_obj": page_obj,
    }

    return render(
        request,
        "catalog/category_detail.html",
        context,
    )


@require_POST
@ratelimit(
    key="ip",
    rate="3/m",
    method="POST",
    block=False,
)
def newsletter_subscribe(request):
    if getattr(request, "limited", False):
        messages.error(
            request,
            _("Too many requests. Please try again later."),
        )
        return redirect("catalog:home")

    raw_email = request.POST.get("newsletterEmail", "")
    email = raw_email.strip().lower()

    if not email:
        messages.error(
            request,
            _("Please enter an email address."),
        )
        return redirect("catalog:home")

    try:
        valid_email_obj = validate_email(
            email,
            check_deliverability=True,
        )

        normalized_email = valid_email_obj.normalized

        user_ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
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
            messages.success(
                request,
                _("Thank you for subscribing to our newsletter."),
            )
        else:
            messages.info(
                request,
                _("You are already subscribed to our email list."),
            )

    except EmailNotValidError as exc:
        logger.warning(
            "Invalid newsletter attempt: %s - Reason: %s",
            email,
            str(exc),
        )
        messages.error(
            request,
            _("Invalid email address. Please check and try again."),
        )

    referer = request.META.get("HTTP_REFERER")

    if referer and url_has_allowed_host_and_scheme(
        referer,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(referer)

    return redirect("catalog:home")