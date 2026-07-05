# Task: Dynamic Views and Currency Conversion

## Files Created

### `catalog/templatetags/currency_tags.py`

- Created a new template tag file to handle currency conversions.
- The `convert_price` tag takes a base price in USD and converts it to the appropriate currency based on the current language.
- It uses Django's caching framework to store exchange rates for one hour, reducing database queries.

## Files Modified

### `catalog/views.py`

- Updated the `home_page` view to fetch the 4 latest active products.
- Used `prefetch_related` for `variants` and `images` to prevent N+1 query issues.

### `templates/includes/latest_products.html`

- Loaded the new `currency_tags` template tag library.
- Updated the product loop to display the dynamic product name and short description.
- Implemented the `convert_price` template tag to show the price of the first product variant in the correct currency.

## Terminal Commands

No terminal commands are required for this task.
