# Task: Frontend Final Polish (Contact UI & Header Nav)

## Files Modified

### `templates/catalog/contact_us.html`
- Replaced the Google Maps implementation with Leaflet.js for a free and open-source map solution.
- Added a `modern-contact-form` class to the contact form and provided the necessary CSS to create a 3D, luxurious appearance.

### `templates/includes/header.html`
- Added a new navigation link for "Terms & FAQ" to the main menu.

## CSS Added to `static/css/custom.css` (or to be added by user)
```css
.modern-contact-form {
    background: var(--color-bg-light);
    border-radius: 15px;
    padding: 30px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.1), 0 5px 15px rgba(138, 96, 156, 0.1);
    border: 1px solid rgba(138, 96, 156, 0.1);
    transform: perspective(1000px) translateZ(0);
    transition: var(--transition-smooth);
}
.modern-contact-form:hover {
    box-shadow: 0 20px 40px rgba(0,0,0,0.15), 0 10px 20px rgba(138, 96, 156, 0.2);
}
html.dark .modern-contact-form {
    background: var(--color-bg-dark-card);
    box-shadow: 0 15px 35px rgba(0,0,0,0.4);
    border: 1px solid rgba(147, 197, 114, 0.1);
}
```

## Terminal Commands
No terminal commands are required for this task.
