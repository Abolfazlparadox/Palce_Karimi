# Task: Refine Catalog Models and Admin

## Files Modified

### `catalog/models.py`

- Created the `ExchangeRate` model to handle currency conversions.
- Enhanced the `ProductVariant` model by adding `base_price` and `stock` fields.
- Updated `Category` and `Product` models to ensure they use `TranslatableModel` correctly and added `verbose_name_plural` to `Category`.
- Improved the `__str__` methods to be more robust.
- Enhanced the `main_image` property to also fetch images from variants.

### `catalog/admin.py`

- Registered the new `ExchangeRate` model.
- Configured `CategoryAdmin` and `ProductAdmin` to inherit from `TranslatableAdmin`.
- Created `ProductVariantInline` and `ProductImageInline` to be displayed within `ProductAdmin`.
- Added `list_display`, `list_filter`, and `search_fields` to `ProductAdmin` and `ProductVariantAdmin` for a better admin experience.
- Added image previews to the image inlines.

## Terminal Commands

The following commands should be executed in a PowerShell terminal:

```pwsh
python manage.py makemigrations catalog
python manage.py migrate
```
