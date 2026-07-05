# Task: Fix Currency Conversion Logic

## Files Modified

### `catalog/templatetags/currency_tags.py`

- Overwrote the entire file with a new, more robust implementation of the `convert_price` template tag.
- The new logic uses `django.utils.translation.get_language()` to securely get the active language.
- It maps the language code to a currency code.
- It fetches exchange rates from the cache or database and provides a clear fallback warning if a rate is missing.
- The formatting is now handled based on the target currency.

## Terminal Commands

No terminal commands are required for this task.
