# Task: Integrate Dynamic Transparent Logos (Light/Dark Mode)

## Files Modified

### `templates/includes/header.html`

- Replaced the `src` attribute of the main logo `<img>` tag with `{% static 'img/logo.webp' %}`.
- Added a second `<img>` tag with the `dark-logo` class and `src` pointing to `{% static 'img/logo-dark.webp' %}` to enable Porto's native dark mode logo switching.
- Updated the `alt` attribute for both logos to use the translatable key `{% trans 'Palace Karimi Logo' %}`.

### `templates/includes/footer.html`

- Replaced the `src` attribute of the footer logo `<img>` tag with `{% static 'img/logo-dark.webp' %}`.
- Updated the `alt` attribute to use the translatable key `{% trans 'Palace Karimi Logo' %}`.

## New Translation Keys

- 'Palace Karimi Logo'
