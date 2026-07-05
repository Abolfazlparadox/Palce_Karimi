# Task: Split Templates

## Directories Created

- `templates/includes/`

## Files Created

### `templates/base.html`

- Created the base template with the main HTML structure, including the header, footer, and a content block.
- All CSS and JavaScript paths were converted to use the `{% static %}` template tag.

### `templates/includes/header.html`

- Extracted the header section from the original `index.html` file.
- All asset paths (images, icons) were converted to use the `{% static %}` template tag.

### `templates/includes/footer.html`

- Extracted the footer section from the original `index.html` file.
- All asset paths (images) were converted to use the `{% static %}` template tag.

## Files Modified

### `templates/index.html`

- The file was rewritten to extend `base.html` and place its content within the `{% block content %}`.
- All asset paths within the content block were converted to use the `{% static %}` template tag.
