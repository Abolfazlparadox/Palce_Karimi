# Task: Fix Split Translations

## Files Modified

### `generate_translations.py`

- Removed the old combined translation key: `'With a rich heritage in cultivating the world’s finest saffron and pistachios, Palace Karimi stands as a bridge between the ancient farms of Persia and the luxury global market. We deliver nothing but perfection.'`
- Added two new distinct translation keys for the split sentence:
    - `'With a rich heritage in cultivating the world’s finest saffron and pistachios, Palace Karimi stands as a bridge between the ancient farms of Persia and the luxury global market.'`
    - `'We deliver nothing but perfection.'`
- Ensured accurate translations for all four languages (fa, en, ar, tr).

## Terminal Commands

The following command should be executed in a PowerShell terminal:

```pwsh
python generate_translations.py
```
