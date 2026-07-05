# Task: Fix Language Switcher Logic

## Files Modified

### `config/urls.py`

- Overwrote the entire file to ensure that `catalog.urls` is only included once within `i18n_patterns`.

### `templates/includes/header.html`

- Replaced the language switcher with a new implementation that uses a hidden form and JavaScript to submit the language change. This avoids conflicts with Porto's JavaScript that was preventing the language from being changed.

## Terminal Commands

No terminal commands are required for this task.
