# Task: Dynamic URL Routing and Dead Link Replacement

## Files Modified

### `templates/includes/header.html`
- Replaced the placeholder `href="#"` for the "Consultation" button with a dynamic URL pointing to the contact page: `{% url 'catalog:contact_us' %}`.
- Verified that all other navigation links (`Home`, `Products`, `About Us`, `Contact Us`) correctly point to their respective named URLs.

### `templates/includes/footer.html`
- Replaced the placeholder `href="#"` for the newsletter form `action` with `{% url 'catalog:contact_us' %}`.
- Replaced the dead link for the footer logo with `{% url 'catalog:home' %}`.
- Updated the "FAQ" link to point to `{% url 'catalog:terms_faq' %}`.
- Updated the "Contact Us" link to point to `{% url 'catalog:contact_us' %}`.
- The "Sitemap" link remains a placeholder as its view has not been created yet.

## Missing Views/URLs

The following view and URL are required for a link in the footer but have not been implemented yet:

- **Sitemap**: A view and corresponding URL pattern named `catalog:sitemap` are needed.
