import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import Category, Product, ProductVariant

def seed():
    # 1. Create Pistachio Category
    pistachio_cat = Category.objects.create(is_active=True)
    pistachio_cat.set_current_language('fa')
    pistachio_cat.name = 'پسته'
    pistachio_cat.slug = 'پسته'
    pistachio_cat.save()

    pistachio_cat.set_current_language('en')
    pistachio_cat.name = 'Pistachio'
    pistachio_cat.slug = 'pistachio'
    pistachio_cat.save()

    pistachio_cat.set_current_language('ar')
    pistachio_cat.name = 'فستق'
    pistachio_cat.slug = 'فستق'
    pistachio_cat.save()

    pistachio_cat.set_current_language('tr')
    pistachio_cat.name = 'Fıstık'
    pistachio_cat.slug = 'fistik'
    pistachio_cat.save()

    # Get the existing Saffron category (created by user) or create if not found
    saffron_cat = Category.objects.translated('fa', name='زعفران').first()
    if not saffron_cat:
        saffron_cat = Category.objects.create(is_active=True)
        saffron_cat.set_current_language('fa')
        saffron_cat.name = 'زعفران'
        saffron_cat.slug = 'زعفران'
        saffron_cat.save()

    # 2. Create Saffron Product
    saffron_prod = Product.objects.create(category=saffron_cat, sku='SAF-SUPER-01', is_active=True)
    saffron_prod.set_current_language('fa')
    saffron_prod.name = 'زعفران سوپر نگین'
    saffron_prod.slug = 'زعفران-سوپر-نگین'
    saffron_prod.short_description = 'بهترین کیفیت زعفران صادراتی'
    saffron_prod.save()
    
    saffron_prod.set_current_language('en')
    saffron_prod.name = 'Super Negin Saffron'
    saffron_prod.slug = 'super-negin-saffron'
    saffron_prod.short_description = 'Premium export quality saffron'
    saffron_prod.save()

    # 3. Create Pistachio Product
    pistachio_prod = Product.objects.create(category=pistachio_cat, sku='PST-AKBARI-01', is_active=True)
    pistachio_prod.set_current_language('fa')
    pistachio_prod.name = 'پسته اکبری دست‌چین'
    pistachio_prod.slug = 'پسته-اکبری'
    pistachio_prod.short_description = 'پسته اکبری درجه یک خندان'
    pistachio_prod.save()

    pistachio_prod.set_current_language('en')
    pistachio_prod.name = 'Akbari Pistachio'
    pistachio_prod.slug = 'akbari-pistachio'
    pistachio_prod.short_description = 'Premium hand-picked Akbari pistachio'
    pistachio_prod.save()

    # 4. Create Variants (no translations needed for now)
    ProductVariant.objects.create(product=saffron_prod, weight='5g', packaging_type='Khatam (خاتم)')
    ProductVariant.objects.create(product=saffron_prod, weight='10g', packaging_type='Crystal (کریستال)')
    
    ProductVariant.objects.create(product=pistachio_prod, weight='500g', packaging_type='Luxury Box')
    ProductVariant.objects.create(product=pistachio_prod, weight='1kg', packaging_type='Vacuum Bag')

    print("Database seeded successfully with multilingual luxury products!")

if __name__ == '__main__':
    seed()
