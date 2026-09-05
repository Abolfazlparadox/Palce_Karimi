"""
Catalog — Critical Production Tests

Minimal, high-value tests covering URL accessibility, language switching,
model constraints, and form validation.
"""

from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import activate

from catalog.models import (
    Category,
    Product,
    ProductVariant,
    TieredPrice,
    ProductImage,
    PackagingType,
    ContactMessage,
    NewsletterSubscriber,
)


class URLAccessibilityTests(TestCase):
    """Verify key public URLs return 200 OK."""

    def setUp(self):
        self.client = Client()

    def test_home_page_fa(self):
        """Persian home page loads."""
        activate('fa')
        resp = self.client.get('/fa/')
        self.assertIn(resp.status_code, (200, 302))

    def test_shop_page_fa(self):
        """Persian shop page loads."""
        activate('fa')
        resp = self.client.get('/fa/shop/')
        self.assertIn(resp.status_code, (200, 302))

    def test_shop_page_en(self):
        """English shop page loads."""
        activate('en')
        resp = self.client.get('/en/shop/')
        self.assertIn(resp.status_code, (200, 302))

    def test_about_page(self):
        """About page loads."""
        resp = self.client.get('/en/about/')
        self.assertIn(resp.status_code, (200, 302))

    def test_contact_page(self):
        """Contact page loads."""
        resp = self.client.get('/en/contact/')
        self.assertIn(resp.status_code, (200, 302))

    def test_nonexistent_product_404(self):
        """Non-existent product slug returns 404."""
        resp = self.client.get('/en/product/nonexistent-slug/')
        self.assertEqual(resp.status_code, 404)

    def test_nonexistent_category_404(self):
        """Non-existent category slug returns 404."""
        resp = self.client.get('/en/category/nonexistent-slug/')
        self.assertEqual(resp.status_code, 404)


class LanguageSwitchingTests(TestCase):
    """Verify language prefix routing works."""

    def test_persian_prefix(self):
        """Persian language prefix resolves."""
        resp = self.client.get('/fa/', HTTP_ACCEPT_LANGUAGE='fa')
        self.assertIn(resp.status_code, (200, 302))

    def test_english_prefix(self):
        """English language prefix resolves."""
        resp = self.client.get('/en/', HTTP_ACCEPT_LANGUAGE='en')
        self.assertIn(resp.status_code, (200, 302))

    def test_arabic_prefix(self):
        """Arabic language prefix resolves."""
        resp = self.client.get('/ar/', HTTP_ACCEPT_LANGUAGE='ar')
        self.assertIn(resp.status_code, (200, 302))

    def test_turkish_prefix(self):
        """Turkish language prefix resolves."""
        resp = self.client.get('/tr/', HTTP_ACCEPT_LANGUAGE='tr')
        self.assertIn(resp.status_code, (200, 302))


class NewsletterFormTests(TestCase):
    """Verify newsletter subscription logic."""

    def test_valid_subscription_creates_record(self):
        """Valid email creates a subscriber."""
        resp = self.client.post(
            '/en/newsletter/subscribe/',
            {'newsletterEmail': 'test@gmail.com'},
            HTTP_REFERER='http://testserver/en/',
        )
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)

    def test_empty_email_rejected(self):
        """Empty email does not create a subscriber."""
        resp = self.client.post(
            '/en/newsletter/subscribe/',
            {'newsletterEmail': ''},
            HTTP_REFERER='http://testserver/en/',
        )
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)

    def test_duplicate_subscription_handled(self):
        """Duplicate email does not create a second record."""
        NewsletterSubscriber.objects.create(email='dup@gmail.com')
        self.client.post(
            '/en/newsletter/subscribe/',
            {'newsletterEmail': 'dup@gmail.com'},
            HTTP_REFERER='http://testserver/en/',
        )
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)

    def test_get_request_not_allowed(self):
        """GET request to newsletter subscribe is rejected."""
        resp = self.client.get('/en/newsletter/subscribe/')
        self.assertEqual(resp.status_code, 405)


class TieredPriceValidationTests(TestCase):
    """Verify tiered pricing business rules."""

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create()
        cls.product = Product.objects.create(category=cls.category)
        cls.pkg = PackagingType.objects.create()
        cls.variant = ProductVariant.objects.create(
            product=cls.product, packaging_type=cls.pkg, sku='TEST-001', weight_in_grams=100
        )

    def test_valid_single_tier(self):
        """Single open-ended tier is valid."""
        tier = TieredPrice(
            product_variant=self.variant, min_qty=1, max_qty=None, price_usd=100
        )
        tier.full_clean()  # Should not raise
        tier.save()
        self.assertEqual(TieredPrice.objects.count(), 1)

    def test_min_greater_than_max_rejected(self):
        """min_qty >= max_qty must raise ValidationError."""
        tier = TieredPrice(
            product_variant=self.variant, min_qty=50, max_qty=49, price_usd=100
        )
        with self.assertRaises(ValidationError):
            tier.full_clean()

    def test_overlapping_tiers_rejected(self):
        """Overlapping quantity ranges must raise ValidationError."""
        TieredPrice.objects.create(
            product_variant=self.variant, min_qty=1, max_qty=49, price_usd=100
        )
        tier = TieredPrice(
            product_variant=self.variant, min_qty=30, max_qty=99, price_usd=90
        )
        with self.assertRaises(ValidationError):
            tier.full_clean()


class ProductImageMainTests(TestCase):
    """Verify only one main image per product."""

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create()
        cls.product = Product.objects.create(category=cls.category)

    def test_main_image_auto_deduplication(self):
        """Setting a new is_main=True clears previous main flag."""
        # We can't test file upload without a mock, but we can verify
        # the save() logic by directly manipulating the model.
        # This test ensures the business rule is enforced.
        img1 = ProductImage.objects.create(
            product=self.product, image='test/path1.webp', is_main=True, order=1
        )
        img2 = ProductImage.objects.create(
            product=self.product, image='test/path2.webp', is_main=True, order=2
        )
        img1.refresh_from_db()
        self.assertFalse(img1.is_main)
        self.assertTrue(img2.is_main)
