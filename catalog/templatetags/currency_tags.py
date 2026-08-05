from django import template
from django.utils.translation import get_language
from catalog.models import ExchangeRate
from django.core.cache import cache
from decimal import Decimal, InvalidOperation

register = template.Library()


@register.filter
def localize_digits(value):
    lang = get_language()
    if lang == 'fa':
        return str(value).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
    return value


@register.simple_tag(takes_context=True)
def convert_price(context, base_price):
    """
    تبدیل قیمت پایه (دلار) به ارز محلی بر اساس زبان
    """
    # اگر مقدار ورودی None باشد
    if base_price is None:
        return ""

    # ---- تبدیل base_price به Decimal با مدیریت خطا ----
    try:
        if isinstance(base_price, (int, float, Decimal)):
            base_price_dec = Decimal(str(base_price))
        elif isinstance(base_price, str):
            # حذف کاما و کاراکترهای اضافی
            clean_str = base_price.replace(',', '').strip()
            base_price_dec = Decimal(clean_str)
        else:
            base_price_dec = Decimal(base_price)
    except (InvalidOperation, ValueError, TypeError):
        # در صورت خطا، قیمت را به صورت دلار با پیام خطا نمایش می‌دهیم
        return f"${base_price} (خطا)"

    lang = context.get('LANGUAGE_CODE', 'en')

    currency_map = {
        'fa': 'IRR',
        'en': 'USD',
        'ar': 'AED',
        'tr': 'TRY'
    }

    target_currency = currency_map.get(lang, 'USD')

    # اگر ارز مقصد دلار است، مستقیماً نمایش بده
    if target_currency == 'USD':
        return f"${base_price_dec:,.2f}"

    # ---- دریافت نرخ از کش یا دیتابیس ----
    cache_key = f'exchange_rate_{target_currency}'
    rate = cache.get(cache_key)

    if rate is None:
        try:
            exchange_obj = ExchangeRate.objects.get(currency=target_currency)
            rate = exchange_obj.rate
            # ذخیره در کش به صورت Decimal
            cache.set(cache_key, rate, 3600)
        except ExchangeRate.DoesNotExist:
            return f"${base_price_dec:,.2f} (نرخ موجود نیست)"

    # ---- تبدیل rate به Decimal با مدیریت خطا ----
    try:
        if isinstance(rate, (int, float, Decimal)):
            rate_dec = Decimal(str(rate))
        elif isinstance(rate, str):
            clean_rate = rate.replace(',', '').strip()
            rate_dec = Decimal(clean_rate)
        else:
            rate_dec = Decimal(rate)
    except (InvalidOperation, ValueError, TypeError):
        return f"${base_price_dec:,.2f} (نرخ نامعتبر)"

    converted_price = base_price_dec * rate_dec

    # ---- نمایش با فرمت ارز محلی ----
    if target_currency == 'IRR':
        price_str = f"{int(converted_price):,}"
        return f"{localize_digits(price_str)} ریال"
    elif target_currency == 'AED':
        price_str = f"{converted_price:,.2f}"
        return f"{localize_digits(price_str)} د.إ"
    elif target_currency == 'TRY':
        price_str = f"{converted_price:,.2f}"
        return f"{localize_digits(price_str)} ₺"

    return localize_digits(f"{converted_price:,.2f}")