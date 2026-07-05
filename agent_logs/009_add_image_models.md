# Task: Add Image Models

## Files Modified

### `requirements.txt`

- Added `Pillow` to the requirements.

```diff
+ Pillow
```

### `catalog/models.py`

- Added the `ProductImage` and `VariantImage` models to support multiple images for products and variants.

### `catalog/admin.py`

- Imported the new `ProductImage` and `VariantImage` models.
- Created `ProductImageInline` and `VariantImageInline` classes.
- Updated `ProductAdmin` and `ProductVariantAdmin` to use the inlines.

## Terminal Commands

The following commands should be executed in a PowerShell terminal:

```pwsh
pip install Pillow
pip freeze > requirements.txt
python manage.py makemigrations catalog
python manage.py migrate
```
