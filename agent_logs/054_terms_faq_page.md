# Task: Create Terms, Conditions & FAQ Page

## Files Created

### `templates/catalog/terms.html`

- Created a new template for the "Terms, Conditions & FAQ" page.
- The template extends `base.html` and uses Porto's Accordion UI for the FAQ section.
- All text is wrapped in `{% trans %}` tags for full multilingual support.

## Files Modified

### `catalog/views.py`

- Added the `terms_faq` view function to render the new `terms.html` template.

### `catalog/urls.py`

- Added a new URL pattern `/terms-and-faq/` that maps to the `terms_faq` view.

## New Translation Keys

Here are the new translation keys that need to be added to `generate_translations.py`:

- 'Terms, Conditions & FAQ'
- 'Shipping & Customs'
- 'Detailed information about our international shipping policies, customs clearance procedures, and delivery times. We ensure a smooth and transparent process for all our global partners.'
- 'Quality Certificates'
- 'All our products are accompanied by internationally recognized quality and safety certificates. Here you can find details about our certifications like ISO, HACCP, and Organic.'
- 'Payment Terms'
- 'We offer flexible and secure payment terms for our B2B partners, including bank transfers, letters of credit, and other arrangements. Contact us to discuss your specific needs.'
- 'Frequently Asked Questions'
- 'What is the minimum order quantity (MOQ)?'
- 'Our MOQ varies depending on the product and packaging. Please contact our sales team for detailed information.'
- 'Do you offer white-labeling services?'
- 'Yes, we offer comprehensive white-labeling and custom packaging solutions for your brand.'
- 'What are the available shipping methods?'
- 'We ship via air, sea, and land freight, depending on the destination and order size.'
