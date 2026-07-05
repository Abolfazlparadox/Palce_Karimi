# Task: Create Catalog Models

## Files Modified

### `config/settings.py`

- Added `'catalog'` to the `INSTALLED_APPS` list.

```diff
+ 'catalog',
```

### `catalog/models.py`

- Created the `catalog/models.py` file with the `Category`, `Product`, and `ProductVariant` models.

### `catalog/admin.py`

- Created the `catalog/admin.py` file and registered the `Category`, `Product`, and `ProductVariant` models with the admin site.

## Terminal Commands

The following commands should be executed in a PowerShell terminal:

```pwsh
python manage.py startapp catalog
python manage.py makemigrations
python manage.py migrate
```
