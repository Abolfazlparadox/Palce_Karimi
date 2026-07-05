# Task: Allow Unicode Slugs and Seed Data

## Files Modified

### `catalog/models.py`

- Updated the `slug` field in both the `Category` and `Product` models to allow Unicode characters.

```diff
-         slug=models.SlugField(),
+         slug=models.SlugField(allow_unicode=True),
```

## Files Created

### `seed_data.py`

- Created a script to populate the database with initial data for categories, products, and product variants in multiple languages.

## Terminal Commands

The following commands should be executed in a PowerShell terminal:

```pwsh
python manage.py makemigrations catalog
python manage.py migrate
python seed_data.py
```
