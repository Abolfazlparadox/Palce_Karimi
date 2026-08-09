# Palace Karimi — Project Audit Report

This document provides a comprehensive technical audit of the Palace Karimi Django project as of its current state. It is intended to serve as a complete context document for developers and AI assistants to plan future work.

---

## 1. Executive Summary

The Palace Karimi project is a **Multilingual B2B Product Catalog** for exporting premium Iranian saffron and pistachios. It is built on a modern, containerized architecture using Django, PostgreSQL, and Nginx. The project's foundation is strong, with excellent implementations for internationalization (i18n), database modeling (`django-parler`), and deployment (Docker).

However, it currently suffers from critical performance issues (N+1 queries), a broken Django Admin theme, and a significant amount of unused frontend assets inherited from its HTML template. The project is a solid "catalog," but lacks any e-commerce functionality like a shopping cart or checkout.

---

## 2. Current Project Stage

**Classification: Backend Mostly Complete, Frontend Integration Stage**

The project is well past the initial setup but is not yet production-ready. The backend models, multilingual framework, and deployment infrastructure are robust. The frontend is a customized template that is functional but not optimized. Core business logic for actual e-commerce is entirely missing.

-   **Completed Components:**
    -   Dockerized production environment (DB, Web, Nginx).
    -   Secure configuration management (`.env`).
    -   Multilingual data models (`django-parler`).
    -   Multilingual URL routing (`i18n_patterns`).
    -   Core catalog views (Shop, Product Detail, Category Detail).
    -   Dynamic, multilingual sitemap and `robots.txt`.
    -   Basic frontend theme with working RTL/LTR and Dark/Light modes.

-   **Partially Completed Components:**
    -   **Django Admin:** The backend logic is there, but the theme is broken due to conflicting CSS overrides.
    -   **Performance:** Views are functional but suffer from severe N+1 query problems.

-   **Missing Components:**
    -   **E-commerce Logic:** No shopping cart, checkout, order management, or user accounts.
    -   **Testing:** No `tests/` directory; zero automated tests.
    -   **CI/CD:** No continuous integration or deployment pipelines.
    -   **API:** No REST API for headless integration.

-   **Production Blockers:**
    -   Critical N+1 performance issues.
    -   Broken Django Admin UI.
    -   Lack of a `collectstatic` step in the `Dockerfile`.
    -   No HTTPS configuration in Nginx.

---

## 3. Architecture Assessment

**Classification: Appropriate and Well-Designed**

The project's architecture is clean and follows Django best practices.

-   **App Responsibilities:**
    -   `config`: Correctly handles project-wide settings and root URL configuration.
    -   `catalog`: Correctly encapsulates all business logic related to the product catalog, from models to views.
    -   `core`: Appropriately placed for future shared utilities, though currently underutilized.
-   **Separation of Concerns:** The separation between the Django application (`web`), database (`db`), and reverse proxy (`nginx`) at the infrastructure level is excellent. Within Django, the `catalog` app is a well-defined, self-contained unit.
-   **SEO & i18n:** The integration of sitemaps, `robots.txt`, `i18n_patterns`, and `django-parler` is architecturally sound.

---

## 4. Database & Models

The database schema defined in `catalog/models.py` is robust and well-suited for a B2B catalog.

-   **Product Structure:** The use of `Product` (for shared data) and `ProductVariant` (for purchasable units) is a flexible and scalable pattern.
-   **Tiered Pricing:** The `TieredPrice` model, linked to `ProductVariant`, is a solid implementation for B2B-specific, quantity-based pricing.
-   **Translation Architecture:** The use of `django-parler` with `TranslatableModel` is the industry standard for multilingual Django models and has been implemented correctly.
-   **Image Optimization:** The use of `django-resized` on the `ProductImage` model to enforce WEBP format and resize images is a significant built-in performance optimization.

**Identified Issues:**

-   **File:** `catalog/models.py`
-   **Problem:** The `Product` model contains two properties, `default_variant` and `main_image`, which fetch related objects.
-   **Impact:** Accessing these properties within a template loop (e.g., on the `shop_page` or `home_page`) without pre-fetching the related objects will trigger a new database query for every single product. This is a classic N+1 query problem.
-   **Severity:** **CRITICAL**
-   **Evidence:**
    ```python
    # In catalog/models.py
    class Product(TranslatableModel):
        ...
        @property
        def default_variant(self):
            # This will run a query for each product in a list.
            variant = self.variants.filter(is_default=True).first()
            return variant if variant else self.variants.first()

        @property
        def main_image(self):
            # This will also run a query for each product.
            img = self.images.filter(is_main=True).first()
            return img if img else self.images.order_by('order').first()
    ```

---

## 5. Django Admin

The Django Admin is **PARTIALLY BROKEN**. While the backend functionality is correctly registered in `catalog/admin.py`, the user interface styling is inconsistent and fails during language switching.

**Investigation of Language-Switching Issue:**

-   **File:** `config/settings.py`
-   **Problem:** The `JAZZMIN_SETTINGS` and `JAZZMIN_UI_TWEAKS` dictionaries still exist, but `'jazzmin'` has been removed from `INSTALLED_APPS`. This is confusing but not the direct cause of the breakage. The settings are simply ignored.

-   **File:** `catalog/admin.py`
-   **Problem:** The `ProductAdmin` class contains a `Media` inner class that explicitly loads an old, likely deleted, CSS file.
-   **Impact:** This hardcoded CSS reference overrides the intended mechanism for loading admin static files and is the most likely cause of styling inconsistencies. The new `static/admin/css/rtl.css` is probably not being loaded at all, or is conflicting with this.
-   **Severity:** **HIGH**
-   **Evidence:**
    ```python
    # In catalog/admin.py
    @admin.register(Product)
    class ProductAdmin(TranslatableAdmin):
        ...
        class Media:
            css = {
                'all': ('css/admin_rtl_fix.css',) # This is incorrect and problematic
            }
    ```

**Desired Behavior Fix:** To fix this, the `Media` class inside `catalog/admin.py` should be removed entirely. The new `static/admin/css/rtl.css` file will be picked up automatically by Django's staticfiles finder if `STATICFILES_DIRS` is configured correctly, which it is.

---

## 6. Static Files Audit

The project's `static/` directory is bloated with unused assets from the Porto HTML template.

-   **USED:**
    -   `static/css/custom.css`: Core custom stylesheet.
    -   `static/css/theme.css`, `theme-elements.css`, `theme-shop.css`: Core Porto styles referenced in `base.html`.
    -   `static/vendor/bootstrap/`, `fontawesome-free/`, `jquery/`: Essential vendor libraries.
    -   `static/js/theme.js`, `theme.init.js`, `custom.js`: Core JavaScript files.
-   **PROBABLY USED:**
    -   `static/vendor/owl.carousel/`, `magnific-popup/`: Used for product image sliders and lightboxes.
-   **UNUSED / SUSPICIOUS:**
    -   **File:** `static/vendor/rs-plugin/` (Revolution Slider)
    -   **Reason:** This is a large, complex slider library. The `home_slider.html` uses its classes, but the project could likely use a simpler slider, reducing bloat.
    -   **Confidence:** HIGH
    -   **File:** `static/js/views/view.home.js`
    -   **Reason:** Contains complex JS for the homepage that may be overkill or partially unused.
    -   **Confidence:** MEDIUM
    -   **File:** `static/vendor/circle-flip-slideshow/`, `jquery.gmap/`, `jquery.easy-pie-chart/`, `vide/`, `vivus/`
    -   **Reason:** These appear to be for specific, complex components of the original template that are not used in the current site.
    -   **Confidence:** HIGH

**Recommendation:** A full audit should be done to trace every single JS and CSS file loaded in `base.html` and remove those not in use. This could significantly improve page load times.

---

## 7. Frontend Technical Audit

The frontend is structurally sound but inefficient.

-   **Template Inheritance:** Correctly uses `{% extends 'base.html' %}`.
-   **Asset Loading:** `base.html` loads a very large number of CSS and JS files, many of which are likely unused (see Section 6). This is the biggest technical issue.
-   **Hardcoded URLs:** The "Designed & Developed by" link in `footer.html` is hardcoded.
-   **RTL/LTR & Dark Mode:** The implementation in `custom.css` using `html[dir="..."]` and `html.dark` selectors is excellent and robust.

---

## 8. Multilingual Architecture

**Classification: Excellent**

The multilingual setup is a key strength.

-   **`django-parler`:** Correctly used for all content models.
-   **`i18n_patterns`:** Correctly used in `config/urls.py` to create language-prefixed URLs (e.g., `/en/`, `/fa/`).
-   **Language Switching:** The language switcher in the header correctly uses Django's `set_language` view.
-   **Sitemaps:** The sitemaps are correctly configured with `i18n = True`, ensuring that search engines can discover all translated versions of each page.

---

## 9. URLs, Views, and SEO

The URL and view structure is logical but was recently incomplete.

-   **Completed Routes:** `home`, `shop`, `product_detail`, `category_products`, `about`, `contact`, `terms_faq`.
-   **SEO:**
    -   `sitemap.xml`: Now correctly configured and functional.
    -   `robots.txt`: Correctly configured and served via `TemplateView`.
    -   **Missing:** The project does not yet implement `hreflang` tags in the `<head>` of each page, which is important for signaling alternate language versions to Google. The `alternates = True` flag in the sitemap classes helps, but `hreflang` tags are also recommended.

---

## 10. Security Audit

The project demonstrates a good understanding of basic Django security.

-   **Secrets Management:** `SECRET_KEY` and `DB_PASSWORD` are correctly managed via `.env` files and are not committed to version control.
-   **CSRF Protection:** Django's CSRF middleware is enabled, and `CSRF_TRUSTED_ORIGINS` is configured via environment variables.
-   **Rate Limiting:** The `newsletter_subscribe` view is protected by `django-ratelimit`, preventing abuse.
-   **File Uploads:** The `ProductImage` model does not appear to have any validation for file type or size, which could be a minor risk. However, `django-resized`'s processing mitigates some of this.
-   **Production Readiness:**
    -   `DEBUG` mode is correctly disabled in production via the `.env` file.
    -   The Nginx configuration does **not** include an SSL/HTTPS setup, which is a **CRITICAL** blocker for production.

---

## 11. Docker / Deployment Audit

**Classification: Near Production-Ready**

The Docker setup is professional and well-architected.

-   **Containerization:** The three-container setup (`db`, `web`, `nginx`) is a standard and robust pattern.
-   **Configuration:** The use of `.env` files and volumes is correct.
-   **Identified Issues:**
    -   **File:** `Dockerfile`
    -   **Problem:** The `Dockerfile` does not contain a `RUN python manage.py collectstatic --no-input` step.
    -   **Impact:** The `web` container will not have the collected static files in `/app/staticfiles/`, and Nginx will fail to serve them, resulting in a broken site.
    -   **Severity:** **CRITICAL**
    -   **File:** `nginx/default.conf`
    -   **Problem:** The configuration only listens on port 80 (HTTP). There is no configuration for port 443 (HTTPS) or SSL certificate management (e.g., Let's Encrypt / Certbot).
    -   **Impact:** The site cannot be served securely in production.
    -   **Severity:** **CRITICAL**
    -   **Missing:** There are no `HEALTHCHECK` instructions in the `Dockerfile` or `docker-compose.yml` to ensure containers are running properly.

---

## 12. Dependencies Audit

The `requirements.txt` file is mostly clean but contains remnants of the abandoned `django-jazzmin` theme.

-   **Unused Dependency:**
    -   `django-jazzmin`: Still listed in some versions of the file, but the app is disabled in settings. This should be removed completely to avoid confusion.

---

## 13. Project Cleanliness

-   **Commented-Out Code:** `config/urls.py` and `config/settings.py` contain commented-out code related to `jazzmin` and incomplete sitemaps, which should be cleaned up.
-   **Old Files:** `static/css/admin_rtl_fix.css` and `static/js/admin_custom.js` are likely obsolete and should be deleted.

---

## 14. Production Readiness Checklist

-   **[PARTIALLY READY]** Django configuration (Needs `DEBUG=False` verification in prod `.env`)
-   **[READY]** Database
-   **[NOT READY]** Static files (Missing `collectstatic` in Dockerfile)
-   **[READY]** Media files
-   **[NOT READY]** Nginx (Missing HTTPS)
-   **[READY]** Gunicorn
-   **[PARTIALLY READY]** Docker (Missing `collectstatic` and health checks)
-   **[NOT READY]** HTTPS
-   **[NOT APPLICABLE]** Domain
-   **[READY]** Environment variables
-   **[PARTIALLY READY]** Security (Needs HTTPS)
-   **[NOT READY]** Logging (Uses basic console logging, no production-grade setup)
-   **[NOT READY]** Backup (No database backup strategy defined)
-   **[PARTIALLY READY]** Error handling (Has 404, but no custom 500 page)
-   **[NOT READY]** Admin (UI is broken)
-   **[READY]** i18n
-   **[READY]** SEO
-   **[NOT READY]** Performance (N+1 queries are a blocker)
-   **[NOT READY]** Monitoring
-   **[NOT READY]** Deployment process (No CI/CD)
-   **[NOT READY]** Update/rollback process

---

## 15. Critical & High Priority Problems

-   **CRITICAL:** Fix N+1 queries in all views by using `select_related` and `prefetch_related`.
-   **CRITICAL:** Add a `RUN python manage.py collectstatic --no-input` step to the `Dockerfile`.
-   **CRITICAL:** Configure Nginx for HTTPS in production.
-   **HIGH:** Fix the broken Django Admin theme by removing the old CSS override from `catalog/admin.py`.
-   **HIGH:** Audit and remove unused CSS/JS assets loaded in `base.html` to improve frontend performance.

---

## 16. Files That Need Attention

-   `catalog/views.py`: For performance optimization.
-   `catalog/admin.py`: To fix the broken admin theme.
-   `Dockerfile`: To add the `collectstatic` command.
-   `nginx/default.conf`: To add HTTPS configuration for production.
-   `templates/base.html`: To remove unused static asset links.

---

## 17. Files That Should Probably Not Be Touched

-   `catalog/models.py`: The data model is well-designed. Changes should be made with care.
-   `docker-compose.yml`: The service orchestration is correct.
-   `.env.example`: The structure is correct.
-   `config/urls.py` (i18n patterns): The multilingual routing is correctly implemented.

---

## 18. Overall Project Status

The project has a very strong and professional architectural foundation but is not yet a complete or production-ready application. It feels like it was built by an experienced backend developer who has now handed it off. The immediate priorities must be to fix the critical performance and deployment blockers. Once stable, it can be extended with actual e-commerce features.

آره، این گزارش برای تصمیم‌گیری اولیه **کافی و نسبتاً خوبه**. ولی یک نکته مهم دارد: من فعلاً این را به‌عنوان **گزارش Gemini** می‌گیرم، نه حقیقت قطعی پروژه. بعضی موارد مثل N+1، `collectstatic` و CSS ادمین باید با خود فایل‌ها تأیید شوند.

با توجه به چیزی که می‌خواهی — **فعلاً Backend و زیرساخت را تمام کنیم و بعد برویم سراغ Frontend** — من پروژه را این‌طور می‌بینم:

## وضعیت فعلی پروژه

تقریباً در مرحله:

**Backend / Architecture → 80–90%**
**Admin → 60–70%**
**Performance → 60–70%**
**Deployment → 60–70%**
**Frontend → فعلاً قابل قبول، نیازمند Polish بعدی**
**Production Ready → هنوز نه**

یعنی پروژه را نباید دوباره از اول بسازی. **مدل‌ها و معماری اصلی را فعلاً دست نزن.**

---

# ترتیب کاری که من پیشنهاد می‌کنم

### Phase 1 — تثبیت Backend

اول این‌ها:

1. بررسی واقعی `catalog/views.py`
2. رفع N+1 Queryها
3. بررسی Queryهای `django-parler`
4. بررسی `select_related` / `prefetch_related`
5. بررسی Pagination
6. بررسی Validation مدل‌ها
7. بررسی Image Upload validation
8. بررسی Admin

این مهم‌ترین مرحله است.

---

# Phase 2 — Admin

Admin برای این پروژه باید **پنل مدیریتی کاربردی** باشد، نه یک داشبورد عجیب و سنگین.

ساختار فعلی مدل‌ها برای Admin مناسب است:

```text
Dashboard
│
├── محصولات
│   ├── محصولات
│   ├── متغیرهای محصول
│   ├── قیمت‌های پلکانی
│   └── تصاویر محصولات
│
├── دسته‌بندی و مشخصات
│   ├── دسته‌بندی‌ها
│   ├── درجات کیفی
│   └── انواع بسته‌بندی
│
├── ارتباطات
│   ├── پیام‌های تماس
│   └── مشترکین خبرنامه
│
└── تنظیمات تجاری
    └── نرخ ارز
```

و چند قابلیت مهم Admin:

### Product

بهتر است بتوانی در یک صفحه:

* اطلاعات فارسی / English / Arabic / Turkish
* Category
* Quality Grade
* SEO
* وضعیت انتشار
* تصاویر
* Variants
* MOQ
* Packaging
* Tiered Pricing

را مدیریت کنی.

این قسمت با مدل فعلی **قابل انجام است**.

---

# یک ایراد مهم در Admin فعلی

این قسمت:

```python
class Media:
    css = {
        'all': ('admin/css/rtl.css',)
    }
```

به احتمال زیاد نباید داخل `ProductAdmin` باشد.

اگر `rtl.css` قرار است **Global Admin CSS** باشد، بهتر است معماری بارگذاری آن درست شود، نه اینکه فقط برای `ProductAdmin` inject شود.

پس این مورد را باید با فایل واقعی `settings.py` و static structure بررسی کنیم.

---

# مشکل Language Switching

این چیزی که گفتی مهم‌تر از ظاهر Admin است.

رفتار مطلوب:

```text
/fa/admin/
    ↓
Admin فارسی
RTL
Theme صحیح
CSS صحیح
JS صحیح


/en/admin/
    ↓
Admin انگلیسی
LTR
همان Theme
همان CSS
همان JS
```

یعنی:

**زبان نباید باعث تغییر Theme شود.**

این را باید به‌عنوان یک requirement مستقل در نظر بگیریم.

---

# Phase 3 — Static Files

اینجا باید عجله نکنیم.

گزارش Gemini گفته تعداد زیادی Asset اضافه وجود دارد. درست.

اما **نباید صرفاً بر اساس اسم فایل حذفشان کنیم.**

مثلاً:

```text
vendor/
├── owl.carousel
├── magnific-popup
├── rs-plugin
├── circle-flip-slideshow
├── jquery.gmap
├── easy-pie-chart
├── vide
└── vivus
```

باید dependency واقعی آنها را پیدا کنیم.

روش درست:

```text
Template
   ↓
base.html
   ↓
CSS / JS
   ↓
Template-specific JS
   ↓
Vendor dependency
```

بعد مشخص کنیم:

```text
KEEP
REMOVE
CONDITIONAL
UNKNOWN
```

**این کار بعد از تثبیت Backend انجام شود.**

---

# Phase 4 — Production

این بخش واقعاً حیاتی است.

حداقل این موارد باید نهایی شوند:

### Docker

```text
nginx
   ↓
gunicorn
   ↓
django
   ↓
postgres
```

و:

```text
collectstatic
migrations
media persistence
static persistence
environment variables
```

### Nginx

باید نهایتاً داشته باشیم:

```text
HTTP
 ↓
HTTPS
 ↓
Nginx
 ↓
Gunicorn
 ↓
Django
```

و:

```text
/static/ → static files
/media/  → media files
```

---

# Phase 5 — Backup

این را Gemini هم درست اشاره کرده.

برای پروژه واقعی شرکت، PostgreSQL بدون Backup مناسب نیست.

حداقل:

```text
PostgreSQL
     ↓
Automated Backup
     ↓
Backup Storage
```

مثلاً روزانه.

حتی اگر پروژه کوچک باشد.

---

# Phase 6 — Logging

لازم نیست برویم سراغ سیستم‌های سنگین Monitoring.

برای این پروژه فعلاً کافی است:

```text
Django logs
Gunicorn logs
Nginx access/error logs
Docker logs
```

و بدانیم اگر سایت خراب شد:

```text
docker compose logs web
docker compose logs nginx
docker compose logs db
```

کجا را بررسی کنیم.

---

# Phase 7 — Testing

اینجا با Gemini کمی اختلاف نظر دارم.

گزارش نوشته:

> Testing: No tests directory; zero automated tests.

ولی برای پروژه کوچک تو، من **پروژه را متوقف نمی‌کنم تا ۸۰٪ coverage بگیری.**

اما صفر تست هم خوب نیست.

حداقل چند تست حیاتی:

```text
Product
Category
ProductVariant
TieredPrice
ContactMessage
Newsletter
```

و مهم‌تر:

```text
URL
Language
Product Detail
Contact Form
Newsletter
Admin permissions
```

حدود **۱۰–۲۰ تست کاربردی** برای این پروژه ارزش زیادی دارند.

---

# یک نکته مهم درباره Models

من فعلاً با گزارش Gemini موافقم که:

> `catalog/models.py` را دست نزن.

مدل‌ها از نظر معماری برای یک **B2B Catalog** منطقی هستند:

```text
Category
   ↓
Product
   ↓
ProductVariant
   ↓
TieredPrice
```

و:

```text
Product
   ↓
ProductImage
```

همچنین:

```text
Product
 ↓
Translations
 ├── fa
 ├── en
 ├── ar
 └── tr
```

ساختار خوبی است.

اما چند مورد باید **Review** شوند، نه اینکه حتماً تغییر کنند:

* `TieredPrice.clean()`
* constraint مربوط به `is_default`
* validation تصاویر
* `Product.main_image`
* `Product.default_variant`
* indexing
* query optimization

---

# چیزهایی که فعلاً انجام نده

برای اینکه پروژه از کنترل خارج نشود:

### فعلاً نرو سراغ:

* REST API
* React
* Vue
* Celery
* Redis
* Kubernetes
* Microservices
* Elasticsearch
* CI/CD پیچیده
* Monitoring حرفه‌ای
* E-commerce
* Payment Gateway
* Cart
* Checkout

چون پروژه فعلی اصلاً به این‌ها نیاز ندارد.

تو یک سایت:

> **Multilingual B2B Company / Product Catalog**

می‌سازی.

نه Digikala.

---

# نقشه نهایی من برای پروژه

اگر بخواهم خیلی ساده اولویت‌بندی کنم:

```text
                    CURRENT
                       │
                       ▼
             ┌──────────────────┐
             │ Backend Audit    │
             │ Views / Queries   │
             └────────┬─────────┘
                      ▼
             ┌──────────────────┐
             │ Fix Performance  │
             │ N+1 / Pagination │
             └────────┬─────────┘
                      ▼
             ┌──────────────────┐
             │ Fix Admin        │
             │ RTL/LTR + UI     │
             └────────┬─────────┘
                      ▼
             ┌──────────────────┐
             │ Static Audit     │
             │ Remove unused    │
             └────────┬─────────┘
                      ▼
             ┌──────────────────┐
             │ Security Review  │
             └────────┬─────────┘
                      ▼
             ┌──────────────────┐
             │ Minimal Tests    │
             └────────┬─────────┘
                      ▼
             ┌──────────────────┐
             │ Docker Production │
             └────────┬─────────┘
                      ▼
             ┌──────────────────┐
             │ Nginx + HTTPS    │
             └────────┬─────────┘
                      ▼
             ┌──────────────────┐
             │ Backup + Logging │
             └────────┬─────────┘
                      ▼
             ┌──────────────────┐
             │ Deploy Server    │
             └────────┬─────────┘
                      ▼
             ┌──────────────────┐
             │ Smoke Test       │
             └────────┬─────────┘
                      ▼
                 PRODUCTION
                      │
                      ▼
             Frontend Polish
```

## مهم‌ترین نکته

**الان پروژه تو در مرحله‌ای نیست که نیاز باشد دوباره معماری‌اش را طراحی کنی.**

مشکل اصلی الان بیشتر این است:

> **Stabilization → Optimization → Admin → Production Hardening → Deployment**

نه:

> Rewrite → New Architecture → New Framework → New Backend

و این تفاوت مهم است.

اگر همین مسیر را بروی، برای یک سایت شرکتی B2B با Django، PostgreSQL و Docker، پروژه کاملاً در محدوده قابل مدیریت است.

### چیزی که پیشنهاد می‌کنم قدم بعدی باشد

گزارش Gemini را فعلاً نگه داریم و **اول `catalog/views.py`، `config/settings.py`، `Dockerfile`، `docker-compose.yml` و `nginx/default.conf` را بررسی کنیم**. این پنج فایل مشخص می‌کنند بخش بزرگی از ادعاهای گزارش واقعاً درست است یا نه.

بعد از آن می‌توانیم یک **Checklist نهایی 1 تا 10** بسازیم و هر مورد را یکی‌یکی ببندیم؛ بدون اینکه وسط کار پروژه را بی‌دلیل پیچیده کنیم.
