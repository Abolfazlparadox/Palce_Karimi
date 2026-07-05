# Task: Customize Header and Implement Language Switcher

## Files Modified

### `config/urls.py`

- Added the `i18n` URL pattern to enable Django's built-in language switching.

```diff
+    path('i18n/', include('django.conf.urls.i18n')),
```

### `templates/includes/header.html`

- Overwrote the entire header with a new structure.
- Added a `<style>` block to apply a custom color theme.
- Replaced the logo and social media links.
- Updated contact information.
- Implemented a language switcher using Django's i18n features.
- Simplified the navigation menu and used the `{% trans %}` tag for menu items.

## Terminal Commands

No terminal commands are required for this task.
