# Task: Eliminate Remaining Inline Styles and Optimize Images

## Files Modified

### `templates/includes/home_slider.html`
- Removed the inline `style="height: 670px;"` from the main slider container and replaced it with the `custom-slider-wrapper` class.

### `templates/includes/home_concept.html`
- Removed all inline styles from the `<span>` and `<strong>` tags.
- Replaced them with the custom CSS classes: `custom-concept-sun` and `custom-concept-label`.
- Corrected the image paths to use the `.webp` extension and the standard `{% static %}` tag, as these are static UI elements.

## CSS Changes (`static/css/custom.css`)

The following CSS rules were intended to be appended to `static/css/custom.css`. Since the file is gitignored, these styles will need to be added manually or the gitignore rule will need to be adjusted.

```css
/* ==========================================
   Home Slider & Concept Component Utilities
   ========================================== */
.custom-slider-wrapper {
    height: 670px;
}
.custom-concept-sun {
    background-color: #C49A3D;
    box-shadow: 0 0 20px rgba(196, 154, 61, 0.5);
}
.custom-concept-label {
    color: #184C36 !important;
    font-size: 16px;
    margin-top: 10px;
    display: block;
}
.our-work {
    color: #D97706 !important;
    border: none !important;
}
```

## Terminal Commands

No terminal commands are required for this task.
