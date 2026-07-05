from django import template
from django.utils.translation import get_language
from catalog.models import ExchangeRate
from django.core.cache import cache

register = template.Library()


@register.simple_tag(takes_context=True)
def convert_price(context, base_price):
    if base_price is None:
        return ""

    # 1. دریافت دقیق زبان از مرورگر یا کانتکست
    request = context.get('request')
    if request and hasattr(request, 'LANGUAGE_CODE'):
        lang = request.LANGUAGE_CODE
    else:
        lang = get_language() or 'en'

    # 2. مپ کردن زبان به کد ارز
    currency_map = {
        'fa': 'IRR',
        'en': 'USD',
        'ar': 'AED',
        'tr': 'TRY'
    }

    target_currency = currency_map.get(lang, 'USD')

    # 3. بازگشت مستقیم دلار برای انگلیسی
    if target_currency == 'USD':
        return f"${base_price:,.2f}"

    # 4. واکشی امن از دیتابیس یا کش
    cache_key = f'exchange_rate_{target_currency}'
    rate = cache.get(cache_key)

    if rate is None:
        try:
            exchange_obj = ExchangeRate.objects.get(currency_code=target_currency)
            rate = exchange_obj.rate_to_base
            cache.set(cache_key, rate, 3600)
        except ExchangeRate.DoesNotExist:
            return f"${base_price:,.2f} (بدون نرخ)"

    # 5. محاسبه و فرمت‌بندی مبلغ
    converted_price = base_price * rate

    if target_currency == 'IRR':
        return f"{int(converted_price):,} ریال"
    elif target_currency == 'AED':
        return f"{converted_price:,.2f} د.إ"
    elif target_currency == 'TRY':
        return f"{converted_price:,.2f} ₺"

    return f"{converted_price:,.2f}"