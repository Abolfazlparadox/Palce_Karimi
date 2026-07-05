# Task: Setup Views and Templates

## Directories Created

- `templates/`
- `static/`
- `media/`

## Files Modified

### `config/settings.py`

- Updated the `TEMPLATES` `DIRS` to `[BASE_DIR / 'templates']`.
- Added `STATICFILES_DIRS`, `MEDIA_URL`, and `MEDIA_ROOT`.

### `catalog/views.py`

- Created the `home_page` view.

### `catalog/urls.py`

- Created the URL patterns for the `catalog` app.

### `config/urls.py`

- Included the `catalog.urls` and added URL patterns for serving media and static files during development.

## Terminal Commands

The following commands should be executed in a PowerShell terminal:

```pwsh
mkdir templates, static, media -ErrorAction SilentlyContinue
```
