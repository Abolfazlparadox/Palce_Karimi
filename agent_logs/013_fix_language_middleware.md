# Task: Fix Language Middleware and HTML Direction

## Files Modified

### `config/settings.py`

- Added `'django.middleware.locale.LocaleMiddleware'` to the `MIDDLEWARE` list in the correct order.

```diff
 MIDDLEWARE = [
     'django.middleware.security.SecurityMiddleware',
     'django.contrib.sessions.middleware.SessionMiddleware',
+    'django.middleware.locale.LocaleMiddleware',
     'django.middleware.common.CommonMiddleware',
     'django.middleware.csrf.CsrfViewMiddleware',
     'django.contrib.auth.middleware.AuthenticationMiddleware',
     'django.contrib.messages.middleware.MessageMiddleware',
     'django.middleware.clickjacking.XFrameOptionsMiddleware',
 ]
```

### `templates/base.html`

- Updated the `<html>` tag to be dynamic based on the current language direction.

```diff
- <html dir="rtl">
+ {% get_current_language_bidi as LANGUAGE_BIDI %}
+ <html {% if LANGUAGE_BIDI %}dir="rtl"{% else %}dir="ltr"{% endif %} lang="{{ LANGUAGE_CODE }}">
```

## Terminal Commands

No terminal commands are required for this task.
