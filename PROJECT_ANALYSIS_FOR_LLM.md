# Project Architecture and Status Report

**Document Purpose:** This report provides a comprehensive architectural overview of the "Palace Karimi" Django project. It is designed to serve as a complete context document for an LLM or external developer, detailing the project's current state, architecture, strengths, and weaknesses without exposing raw source code.

---

## 1. Executive Summary & Tech Stack

The project is a **Multilingual B2B Export Platform** for luxury Iranian goods, specifically Saffron and Pistachios. It is built as a modern, containerized web application with a strong focus on internationalization and a clean, production-ready architecture.

**Core Technology Stack:**
- **Backend Framework:** Django 5.2+
- **Programming Language:** Python 3.12
- **Database:** PostgreSQL 16
- **Web Server / Reverse Proxy:** Nginx
- **Application Server:** Gunicorn
- **Containerization:** Docker & Docker Compose
- **Multilingual Content:** `django-parler`
- **Multilingual UI:** Django's built-in `i18n` framework (`gettext`)
- **Admin Theme:** `django-jazzmin` (Note: Currently commented out in `INSTALLED_APPS` but fully configured)
- **Image Handling:** `django-resized` for automatic optimization and format conversion.
- **Other Key Libraries:** `python-dotenv`, `django-rosetta`, `psycopg2-binary`.

---

## 2. Directory & Architecture Structure

The project follows a clean and standard Django layout.

- **`config/`**: The main project configuration app. It manages global settings (`settings.py`), root URL routing (`urls.py`), and the WSGI entry point.
- **`catalog/`**: The core business logic application. It is responsible for:
    - **Models:** All data models related to products, categories, pricing, and user interactions.
    - **Views:** All public-facing views for the website (home, shop, about, contact).
    - **URLS:** App-specific routing.
    - **SEO:** Contains the `sitemap.py` definitions.
- **`core/`**: A standard app for project-wide utilities, custom management commands, or abstract base models. Its current usage appears minimal.
- **`nginx/`**: Contains the Nginx configuration file (`default.conf`) used by the Docker setup to manage web traffic.
- **`templates/`**: Global templates directory, including `base.html` and the `robots.txt` file.
- **`static/`**: Global directory for frontend assets (CSS, JS, images).

---

## 3. Data Models & Database Schema

The database schema is well-structured for a B2B e-commerce catalog, with a strong emphasis on multilingual content via `django-parler`.

- **Core Product Models:**
    - **`Product`**: The central entity, containing translatable fields like `name`, `slug`, and `description`.
    - **`Category`**, **`QualityGrade`**, **`PackagingType`**: Translatable taxonomy models used to classify products.
    - **`ProductVariant`**: Represents a specific, purchasable version of a product, defined by its weight and packaging. It holds the SKU and MOQ (Minimum Order Quantity).
    - **`TieredPrice`**: A child of `ProductVariant`, defining quantity-based pricing (e.g., price for 1-10 units, 11-50 units, etc.). This is essential for B2B logic.
    - **`ProductImage`**: Manages product imagery. It leverages `django-resized` to automatically convert uploaded images to the efficient **WEBP** format and resize them, which is a major performance strength.

- **Operational Models:**
    - **`ContactMessage`**: Stores messages from the site's contact form.
    - **`NewsletterSubscriber`**: Stores emails of users who subscribe to the newsletter.
    - **`ExchangeRate`**: A model to store currency conversion rates, indicating a multi-currency feature is planned or active.

- **`django-parler` Implementation:** All translatable models (`Product`, `Category`, etc.) use `TranslatableModel` and `TranslatedFields`. This creates separate, dedicated tables in the database (e.g., `catalog_product_translation`) for each language, which is a scalable and efficient approach.

---

## 4. Infrastructure & Deployment Configuration

The project is fully containerized with a professional, production-ready Docker setup.

- **`docker-compose.yml`:** Defines a three-service architecture:
    1.  **`db`**: A PostgreSQL 16 container for the database.
    2.  **`web`**: The Django application container, running Gunicorn as the application server.
    3.  **`nginx`**: An Nginx container acting as a reverse proxy.
- **`Dockerfile`:** Builds the `web` container. It correctly uses a slim Python image, installs system dependencies (`libpq-dev` for PostgreSQL), installs Python packages from `requirements.txt`, and copies the application code.
- **Container Interaction:**
    - The `nginx` container is the public entry point, listening on port 80.
    - It serves static and media files directly from shared volumes for high performance.
    - All other requests are proxied to the `web` (Gunicorn) container on its internal port 8000.
    - The `web` container communicates with the `db` container over the internal Docker network.
- **Data Persistence:** Named volumes (`postgres_data`, `static_volume`, `media_volume`) are used to ensure that database data, static files, and user-uploaded media persist even if the containers are destroyed and recreated.
- **Environment Variables:** The configuration is securely managed via a `.env` file, which is properly ignored by Git. The `docker-compose.yml` file correctly injects these variables into the `db` and `web` containers, separating configuration from code.

---

## 5. Strengths & Completed Work (Positives)

- **Excellent Infrastructure:** The Docker and Nginx setup is robust, scalable, and follows modern best practices for deploying Django applications.
- **Secure Configuration:** The use of `.env` files for managing secrets and environment-specific settings is a major strength.
- **Solid Multilingual Foundation:** The combination of `django-parler` for data and `i18n_patterns` for URLs is the correct and most powerful way to build a multilingual Django site.
- **Advanced SEO Implementation:** The sitemap is correctly configured to be multilingual (`i18n=True`), and the `robots.txt` is served efficiently via a template.
- **Performance-Oriented Image Handling:** Automatic resizing and conversion of images to WEBP via `django-resized` is a proactive performance optimization.
- **Well-Designed Admin:** The Django admin is thoughtfully configured with `fieldsets` and `inlines` to provide a good user experience for content managers.

---

## 6. Weaknesses, Missing Features & Technical Debt (Negatives)

- **CRITICAL - Missing Core Views:**
    - **No Product Detail Page:** The `catalog/urls.py` file is missing a URL pattern and corresponding view for displaying a single product (e.g., `/product/<slug>/`). This is a fundamental gap in an e-commerce site.
    - **No Category Page:** There is no URL or view for listing products belonging to a specific category.
    - **Impact:** This is the direct cause of the `NoReverseMatch` error when the sitemap framework tries to generate URLs for products and categories. The sitemap logic itself is correct, but the URLs it needs to point to do not exist.
- **Incomplete E-commerce Functionality:** The project is currently a "catalog," not a store. It lacks:
    - Shopping Cart and "Add to Cart" functionality.
    - A checkout process.
    - User accounts for B2B clients to manage orders and view pricing.
    - An order management system in the backend.
- **No API Layer:** There is no REST API (e.g., using Django Rest Framework). This limits the ability to integrate with modern JavaScript frontends or mobile applications.
- **Complete Lack of Testing:** There is no evidence of a `tests/` directory or any unit, integration, or end-to-end tests. This is a significant risk that makes future development and refactoring unsafe.
- **No CI/CD Pipeline:** The project lacks automation for testing and deployment. All deployments are likely manual.
- **Deactivated Admin Theme:** The `jazzmin` app is currently commented out in `settings.py`, meaning the advanced admin theme is not active.
- **Incomplete Sitemap Configuration:** The `ProductSitemap` and `CategorySitemap` are commented out in `config/urls.py`, hiding the `NoReverseMatch` error but also leaving the sitemap incomplete.

---

## 7. Security & Performance Audit

- **Performance - N+1 Query Risk:**
    - The `shop_page` view fetches a list of products but does not pre-fetch related data. When the template accesses `product.main_image` or `product.default_variant.base_price` inside a loop, it will trigger a new database query for every single product, leading to a severe N+1 performance bottleneck.
    - **Recommendation:** The query should be optimized using `select_related` for ForeignKey relationships (like `category`) and `prefetch_related` for reverse or ManyToMany relationships (like `images`, `variants`, `tiered_prices`).
- **Performance - Caching:** There is no caching strategy implemented (e.g., Redis, Memcached). High-traffic pages and complex database queries are not cached, which will limit scalability.
- **Security:**
    - The project uses Django's built-in CSRF protection, and `CSRF_TRUSTED_ORIGINS` is correctly configured.
    - The use of `django-ratelimit` on the newsletter subscription form is a good measure against abuse.
    - However, there is no implementation of more advanced security headers like `Content-Security-Policy` (CSP), which would help mitigate XSS attacks.
    - The `DEBUG` flag is correctly read from the `.env` file, reducing the risk of it being `True` in production, but this depends on disciplined environment management.