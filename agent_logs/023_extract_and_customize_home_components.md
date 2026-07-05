# Task: Extract and Customize Home Components

## Files Created

### `templates/includes/home_intro.html`

- Created a new template file for the "home-intro" section.
- The content has been rewritten to match the Palace Karimi brand and is fully multilingual.

### `templates/includes/home_features.html`

- Created a new template file for the "word-rotator" section.
- The content has been rewritten to match the Palace Karimi brand and is fully multilingual.

## Files Modified

### `templates/index.html`

- Removed the hardcoded "home-intro" and "word-rotator" sections.
- Added `{% include %}` tags to load the new template files.

### `templates/base.html`

- Added CSS override rules to the `<style>` block to ensure the correct color palette is applied to the new components.

### `generate_translations.py`

- Updated the `translations` dictionary to include all the new strings from the `home_intro.html` and `home_features.html` templates.

## Terminal Commands

The following command should be executed in a PowerShell terminal:

```pwsh
python generate_translations.py
```
