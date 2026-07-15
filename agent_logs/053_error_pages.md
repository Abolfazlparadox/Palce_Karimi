# Task: Create Standard Error Pages (404 & 500)

## Files Created

### `templates/404.html`

- Created a new template for the 404 "Page Not Found" error.
- The template extends `base.html` and uses Porto's clean UI to display a user-friendly error message.
- All text is wrapped in `{% trans %}` tags for full multilingual support.

### `templates/500.html`

- Created a new template for the 500 "Internal Server Error".
- The template extends `base.html` and provides a professional message for server-side issues.
- All text is wrapped in `{% trans %}` tags.

## How to Test

To test the new error pages, you can temporarily modify your `config/settings.py`:

1.  **For 404 errors**: Set `DEBUG = False` and add `ALLOWED_HOSTS = ['*']`. Then, navigate to a non-existent URL (e.g., `/this-page-does-not-exist/`).
2.  **For 500 errors**: You can create a temporary view that intentionally raises an exception:
    ```python
    # In catalog/views.py
    def test_500(request):
        raise Exception("This is a test 500 error.")
    
    # In catalog/urls.py
    path('test-500/', views.test_500, name='test_500'),
    ```
    Then navigate to `/test-500/` with `DEBUG = False`.

**Remember to revert these changes after testing.**

## New Translation Keys

Here are the new translation keys that need to be added to `generate_translations.py`:

- '404 - Page Not Found'
- '404'
- 'Oops! The page you were looking for doesn’t exist.'
- 'You may have mistyped the address or the page may have moved.'
- 'Back to Home'
- '500 - Internal Server Error'
- '500'
- 'We are currently experiencing technical difficulties.'
- 'Please try again later or contact support if the problem persists.'
