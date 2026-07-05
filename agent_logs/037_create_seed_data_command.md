# Task: Create Seed Data Command

## Files Created

### `catalog/management/commands/seed_data.py`

- Created a new Django management command to seed the database with realistic dummy data.
- The script clears existing data to prevent duplicates.
- It creates `ExchangeRate` objects for multiple currencies.
- It creates `Category` and `Product` objects with translations for four languages (English, Persian, Arabic, and Turkish) using `django-parler`.
- It creates `ProductVariant` objects with base prices and stock levels for each product.

## Terminal Commands

The following command should be executed in a PowerShell terminal:

```pwsh
python manage.py seed_data
```
