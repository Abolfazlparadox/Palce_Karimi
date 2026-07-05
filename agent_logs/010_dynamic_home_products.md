# Task: Display Latest Products on Home Page

## Files Modified

### `catalog/views.py`

- Updated the `home_page` view to fetch the 4 newest products.
- The `latest_products` variable is passed to the template context.

```diff
+    latest_products = Product.objects.filter(is_active=True).prefetch_related('translations', 'images').order_by('-created_at')[:4]
...
     context = {
         'products': products,
         'categories': categories,
+        'latest_products': latest_products,
     }
```

### `templates/index.html`

- Added a new section to display the latest products using a `for` loop.
- The product card design is based on the `shop-4-columns.html` template.
- Includes a fallback for products without images.

## Terminal Commands

No terminal commands are required for this task.
