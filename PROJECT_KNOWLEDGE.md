# Project Knowledge Base: Palace Karimi

This document provides a comprehensive architectural overview of the Palace Karimi Django project. It is intended to be the primary context guide for any AI or human developer working on this codebase.

---

## 1. Project Overview

-   **Project Name**: Palace Karimi
-   **Core Objective**: A multilingual, multi-currency B2B e-commerce platform for exporting luxury Iranian products, specifically Saffron and Pistachios.
-   **Key Features**:
    -   Product catalog with complex variants and tiered pricing.
    -   Multilingual support for UI and database content (fa, en, ar, tr).
    -   RTL/LTR layout switching based on the selected language.
    -   Dark/Light mode theme support.
    -   Customized Django Admin panel for efficient content management.

---

## 2. Technology Stack

-   **Backend**:
    -   **Language**: Python 3.12+
    -   **Framework**: Django 5.2+
-   **Frontend**:
    -   **Template**: Porto HTML Template (heavily customized).
    -   **Styling**: Bootstrap (via Porto), with extensive overrides in `static/css/custom.css`.
    -   **JavaScript**: jQuery, with custom scripts for theme toggling and UI interactions.
-   **Database**:
    -   **Production**: PostgreSQL (via Docker).
    -   **Development**: SQLite (as per standard Django setup, but Postgres is preferred).
-   **Key Third-Party Libraries**:
    -   `django-jazzmin`: For a modern, configurable admin theme.
    -   `django-parler`: For multilingual database model translations.
    -   `rosetta`: For in-browser editing of `.po` translation files.

---

## 3. Directory & App Structure

-   **Project Root**: `D:/Project/Palce_Karimi_v1/`
-   **Configuration App**: `config/` (contains `settings.py`, `urls.py`, etc.)
-   **Local Apps**:
    -   `core/`: Likely for project-wide utilities, management commands, or base models.
    -   `catalog/`: The primary application managing all e-commerce and content logic (products, categories, contacts).
-   **Static & Template Folders**:
    -   `static/`: Contains all frontend assets (CSS, JS, images). The most important file is `static/css/custom.css`, which controls the entire visual identity.
    -   `templates/`: Contains all Django templates. It uses a standard `base.html` with `includes/header.html` and `includes/footer.html`.
    -   `locale/`: Stores the `.po` and `.mo` files for UI string translations.

---

## 4. Database Schema (`catalog/models.py`)

The database is designed around a core `Product` model with several related models for variations and attributes. `django-parler` is used extensively for translatable fields.

-   **`Product`**: The central model.
    -   **Translated Fields**: `name`, `slug`, `short_description`, `full_description`, SEO fields.
    -   **Relationships**:
        -   `ForeignKey` to `Category`.
        -   `ForeignKey` to `QualityGrade`.
-   **`ProductVariant`**: Represents a specific version of a `Product`.
    -   **Purpose**: Defines a purchasable unit based on weight and packaging.
    -   **Fields**: `weight_in_grams`, `sku`, `moq` (Minimum Order Quantity).
    -   **Relationships**:
        -   `ForeignKey` to `Product`.
        -   `ForeignKey` to `PackagingType`.
-   **`TieredPrice`**: Defines the B2B pricing structure.
    -   **Purpose**: Allows for different prices based on the quantity purchased.
    -   **Fields**: `min_qty`, `max_qty`, `price_usd`.
    -   **Relationships**: `ForeignKey` to `ProductVariant`.
-   **Taxonomy Models**:
    -   `Category`: Translatable name and slug.
    -   `QualityGrade`: Translatable name (e.g., 'Super Premium').
    -   `PackagingType`: Translatable name (e.g., '1 kg box').
-   **Other Models**:
    -   `ProductImage`: Stores product images with an `order` field and an `is_main` flag.
    -   `ContactMessage`: Stores submissions from the contact form.
    -   `ExchangeRate`: Stores currency conversion rates against a base currency.

---

## 5. Translation & Internationalization (i18n)

The project uses a dual approach for multilingual support:

1.  **UI Translations (`gettext`)**:
    -   Standard Django `{% trans "string" %}` tags are used in templates.
    -   `LOCALE_PATHS` in `settings.py` points to the `locale/` directory.
    -   A custom `generate_translations.py` script likely automates the `makemessages` and `compilemessages` process.
2.  **Database Content Translations (`django-parler`)**:
    -   Models like `Product`, `Category`, etc., inherit from `TranslatableModel`.
    -   Translatable fields are wrapped in a `TranslatedFields` block.
    -   This creates separate database tables to hold translations for each language (`catalog_product_translation`, etc.).
    -   **CRITICAL**: The `__str__` method on these models uses `self.safe_translation_getter('name', any_language=True)` to prevent crashing in the admin if a translation is missing.

---

## 6. Admin Panel Customizations (`jazzmin` & `catalog/admin.py`)

The admin panel is heavily customized for a better user experience.

-   **Theme**: `django-jazzmin` is used, with extensive configuration in `JAZZMIN_SETTINGS` and `JAZZMIN_UI_TWEAKS`.
-   **Branding**: Custom logos, titles, and a welcome sign are configured.
-   **Layout**:
    -   The `changeform_format` is set to `horizontal_tabs` for most models, making it easy to switch between languages when editing content.
    -   `ProductAdmin` uses `inlines` for `ProductImage` and `ProductVariant`, allowing variants and images to be managed directly from the product page.
    -   `fieldsets` are used to group related fields logically (e.g., "SEO", "Publishing").
-   **Custom Actions**: `make_published` and `make_unpublished` actions are available on the `Product` list view to bulk-update product visibility.
-   **RTL Fixes**: A custom CSS file (`admin_rtl_fix.css`) is loaded to ensure the admin panel renders correctly in Persian/Arabic.

---

## 7. Frontend Architecture

The frontend is built on the Porto template but with significant architectural decisions implemented in `custom.css`.

-   **CSS Variables**: A modern color system using CSS variables (`--color-primary`, `--color-pistachio`, etc.) is defined at the `:root` level. This makes theme changes trivial.
-   **Dark Mode**:
    -   A `dark` class on the `<html>` element triggers all dark mode styles.
    -   JavaScript in `base.html` handles toggling this class and saving the user's preference in `localStorage`.
    -   The CSS contains a dedicated section (`html.dark ...`) that overrides colors for backgrounds, text, and components.
-   **RTL/LTR Logic**:
    -   The `<html>` tag's `dir` attribute is dynamically set based on `LANGUAGE_CODE`.
    -   `custom.css` contains extensive rules using `html[dir="ltr"]` and `html[dir="rtl"]` selectors to mirror the layout. This includes floating elements, text alignment, padding, and even breadcrumb separators.
    -   **Font Management**: A specific font (`Poppins`) is applied only to LTR languages to differentiate them from the default Persian font.

---

## 8. Strict Rules & Guardrails

1.  **NEVER Modify Vendor CSS**: All style changes **MUST** be made in `static/css/custom.css`. Do not edit `theme.css` or any Bootstrap files directly.
2.  **Respect the CSS Variable System**: When adding new components, use the existing CSS variables (`--color-primary`, `--color-bg-dark`, etc.) instead of hardcoding hex codes.
3.  **Use Translatable Model `__str__` Safely**: Any new model using `django-parler` **MUST** use `self.safe_translation_getter('field', any_language=True)` in its `__str__` method to avoid admin crashes.
4.  **Preserve RTL/LTR Mirroring**: When adding new UI components, ensure they are correctly mirrored using `html[dir="ltr"]` and `html[dir="rtl"]` selectors in `custom.css`.
5.  **Use `gettext` for All Static UI Text**: Any user-visible string in a template must be wrapped in `{% trans "..." %}`.
6.  **Follow Admin Inline/Fieldset Patterns**: When adding new models to the admin, follow the existing patterns of using `inlines` and `fieldsets` for a consistent UX.

---

## 9. Observed Technical Debt & Missing Components

-   **No Automated Testing**: There is no evidence of a `tests/` directory or any unit/integration tests. This is a significant risk.
-   **Hardcoded URLs**: The footer contains a hardcoded link to a GitHub profile. This should be a template variable or a setting.
-   **Sitemap is a Dead Link**: The sitemap link in the footer (`#`) is not implemented.
-   **No Caching Strategy**: There is no evidence of a caching framework (e.g., Redis, Memcached) being configured, which will be critical for performance.
-   **Security**: `SECRET_KEY` is hardcoded and visible. `DEBUG` is set to `True`. These need to be managed via environment variables for production.
-   **Database Password**: The database password is hardcoded in `settings.py`. This is a major security vulnerability.
-   **Newsletter Form**: The newsletter form in the footer submits to the contact page, which is likely incorrect. It should have its own dedicated view and logic.
