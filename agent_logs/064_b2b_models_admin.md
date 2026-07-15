# Task: Implement B2B Export Database Models & Admin

## Files Modified

### `catalog/models.py`

- Completely overhauled the database schema to support a robust B2B export platform.
- Created new translatable models: `QualityGrade` and `PackagingType`.
- Enhanced the `Product` model with translatable SEO fields and a foreign key to `QualityGrade`.
- Refactored `ProductVariant` to link to `PackagingType` and include fields for `weight_in_grams`, `moq`, and `is_default`.
- Introduced a `TieredPrice` model to allow for complex pricing structures based on quantity, linked to `ProductVariant`.
- Ensured all translatable models use `django-parler` and have safe `__str__` methods.

### `catalog/admin.py`

- Registered all new models (`QualityGrade`, `PackagingType`, `TieredPrice`).
- Configured `TranslatableAdmin` for all translatable models.
- Implemented `StackedInline` for `ProductVariant` and `TabularInline` for `TieredPrice` and `ProductImage`.
- Embedded the inlines within `ProductAdmin` to provide a seamless content management experience, allowing variants, images, and tiered prices to be managed directly from the product page.
- Added comprehensive `list_display`, `list_filter`, and `search_fields` to all relevant models to improve admin usability.

## Terminal Commands

The following commands should be executed in a PowerShell terminal to apply the new database schema:

```pwsh
python manage.py makemigrations catalog
python manage.py migrate
```
