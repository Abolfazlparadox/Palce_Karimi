from django import template
from django.utils.translation import get_language
from catalog.models import ExchangeRate
from django.core.cache import cache

register = template.Library()

@register.filter
def localize_digits(value):
    lang = get_language()
    if lang == 'fa':
        return str(value).translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
    return value

@register.simple_tag(takes_context=True)
def convert_price(context, base_price):
    if base_price is None:
        return ""

    lang = context.get('LANGUAGE_CODE', 'en')
    
    currency_map = {
        'fa': 'IRR',
        'en': 'USD',
        'ar': 'AED',
        'tr': 'TRY'
    }
    
    target_currency = currency_map.get(lang, 'USD')
    
    if target_currency == 'USD':
        return f"${base_price:,.2f}"

    cache_key = f'exchange_rate_{target_currency}'
    rate = cache.get(cache_key)
    
    if rate is None:
        try:
            exchange_obj = ExchangeRate.objects.get(currency_code=target_currency)
            rate = exchange_obj.rate_to_base
            cache.set(cache_key, rate, 3600)
        except ExchangeRate.DoesNotExist:
            return f"${base_price:,.2f} (Rate Missing)"
            
    converted_price = base_price * rate
    
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
