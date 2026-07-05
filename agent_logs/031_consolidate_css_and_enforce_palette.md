# Task: Consolidate CSS and Enforce Palette

## Files Modified

### `templates/base.html`
- Removed the inline `<style>` block.
- Added a `<link>` tag to the new external stylesheet `palace_karimi.css` just before the closing `</head>` tag.

### `templates/includes/header.html`
- Removed the inline `<style>` block.

### `templates/includes/footer.html`
- Removed the inline `<style>` block.

### `templates/includes/home_concept.html`
- Removed the inline `<style>` block.

### `templates/includes/latest_products.html`
- This file was already created without a `<style>` block, so no changes were needed.

## Files Created

### `static/css/palace_karimi.css`
- Created a new CSS file to consolidate all the scattered styles from the various templates.
- Audited and enforced the official Palace Karimi color palette throughout the file, replacing all default Porto colors.
- Placed the Vazirmatn font `@import` at the top of the file.

## Terminal Commands

No terminal commands are required for this task.
