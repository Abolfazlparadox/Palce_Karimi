# Task: Fix Hover Blue and Create Home Concept

## Files Modified

### `templates/base.html`

- Added a new set of CSS rules to the `<style>` block to globally override Porto's default blue hover color on links and dropdown items.
- Added styles to correctly apply the Palace Karimi color palette to the `.home-concept` section and Owl Carousel dots.

### `templates/includes/header.html`

- Replaced the language switcher with a standard Bootstrap dropdown to ensure it is always visible and functional.

### `templates/index.html`

- Replaced the hardcoded `.home-concept` section with an `{% include %}` tag for the new `home_concept.html` template.

### `generate_translations.py`

- Updated the `translations` dictionary to include the new strings from the `home_concept.html` template.

## Files Created

### `templates/includes/home_concept.html`

- Created a new template file for the "home-concept" section, with content tailored for the Palace Karimi brand and fully multilingual.

## Terminal Commands

No terminal commands are required for this task.
