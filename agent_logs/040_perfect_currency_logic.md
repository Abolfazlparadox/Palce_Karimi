# Task: Perfect Currency Conversion Logic

## Files Modified

### `catalog/templatetags/currency_tags.py`

- Overwrote the entire file to revert to using `takes_context=True` for the `convert_price` template tag.
- This ensures that the active language is correctly retrieved from the template's context, fixing the bug where the currency would not switch dynamically.
- The robust database fetching, caching, and fallback logic from the previous iteration have been preserved.

## Terminal Commands

No terminal commands are required for this task.
