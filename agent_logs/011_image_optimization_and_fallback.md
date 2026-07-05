# Task: Image Optimization and Fallback

## Files Created

### `catalog/utils.py`

- Created a utility file for image processing and generating smart upload paths.
- `optimize_image`: Converts images to WebP and resizes them.
- `product_image_path`, `variant_image_path`: Generate unique, organized paths for uploaded images.

## Files Modified

### `catalog/models.py`

- Imported the new utility functions.
- Added a `main_image` property to the `Product` model to intelligently find the best image to display (product image, then variant image).
- Updated `ProductImage` and `VariantImage` models to use the new `upload_to` functions.
- Added a custom `save` method to both `ProductImage` and `VariantImage` to automatically call the `optimize_image` function.

### `templates/index.html`

- Updated the product display loop to use the new `product.main_image` property, ensuring a fallback mechanism is in place.

## Terminal Commands

The following commands should be executed in a PowerShell terminal:

```pwsh
python manage.py makemigrations catalog
python manage.py migrate
```
