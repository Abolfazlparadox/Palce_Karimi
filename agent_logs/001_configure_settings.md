# Task: Configure Django Settings

## Files Modified

### `requirements.txt`

- Appended `django-parler` and `django-rosetta` to the file.

```diff
+ django-parler
+ django-rosetta
```

### `config/settings.py`

- Added `'core'`, `'parler'`, and `'rosetta'` to `INSTALLED_APPS`.
- Updated the `DATABASES` dictionary to use PostgreSQL with placeholder credentials.
- Configured i18n settings:
    - Set `LANGUAGE_CODE` to `'fa'`.
    - Set `USE_I18N` to `True`.
    - Set `USE_TZ` to `True`.
    - Added the `LANGUAGES` tuple.
    - Added `LOCALE_PATHS`.
    - Added Parler default settings.

## Terminal Commands

The following commands should be executed in a PowerShell terminal:

```pwsh
pip install -r requirements.txt
mkdir locale
```
