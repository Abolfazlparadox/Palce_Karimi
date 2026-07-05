from django.core.management.base import BaseCommand
from catalog.models import Category, Product, ProductVariant, ExchangeRate

class Command(BaseCommand):
    help = 'Seeds the database with Palace Karimi dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        ExchangeRate.objects.all().delete()
        Category.objects.all().delete()
        Product.objects.all().delete()

        self.stdout.write('Creating Exchange Rates...')
        ExchangeRate.objects.create(currency_code='USD', rate_to_base=1.00)
        ExchangeRate.objects.create(currency_code='IRR', rate_to_base=600000.00)
        ExchangeRate.objects.create(currency_code='AED', rate_to_base=3.67)
        ExchangeRate.objects.create(currency_code='TRY', rate_to_base=32.50)

        self.stdout.write('Creating Categories & Products...')
        # Saffron Category
        cat_saffron = Category.objects.create(is_active=True)
        cat_saffron.set_current_language('en')
        cat_saffron.name = 'Saffron'
        cat_saffron.slug = 'saffron'
        cat_saffron.save()
        
        cat_saffron.set_current_language('fa')
        cat_saffron.name = 'زعفران'
        cat_saffron.slug = 'saffron-fa'
        cat_saffron.save()

        cat_saffron.set_current_language('ar')
        cat_saffron.name = 'زعفران'
        cat_saffron.slug = 'saffron-ar'
        cat_saffron.save()

        cat_saffron.set_current_language('tr')
        cat_saffron.name = 'Safran'
        cat_saffron.slug = 'safran-tr'
        cat_saffron.save()

        # Pistachio Category
        cat_pistachio = Category.objects.create(is_active=True)
        cat_pistachio.set_current_language('en')
        cat_pistachio.name = 'Pistachio'
        cat_pistachio.slug = 'pistachio'
        cat_pistachio.save()

        cat_pistachio.set_current_language('fa')
        cat_pistachio.name = 'پسته'
        cat_pistachio.slug = 'pistachio-fa'
        cat_pistachio.save()

        cat_pistachio.set_current_language('ar')
        cat_pistachio.name = 'فستق'
        cat_pistachio.slug = 'pistachio-ar'
        cat_pistachio.save()

        cat_pistachio.set_current_language('tr')
        cat_pistachio.name = 'Fıstık'
        cat_pistachio.slug = 'fistik-tr'
        cat_pistachio.save()

        # Products
        # Super Negin Saffron
        prod_super_negin = Product.objects.create(category=cat_saffron, sku='PK-SAF-SN-01', is_active=True)
        prod_super_negin.set_current_language('en')
        prod_super_negin.name = 'Super Negin Saffron'
        prod_super_negin.slug = 'super-negin-saffron'
        prod_super_negin.short_description = 'The highest quality saffron in the world.'
        prod_super_negin.save()

        prod_super_negin.set_current_language('fa')
        prod_super_negin.name = 'زعفران سوپر نگین'
        prod_super_negin.slug = 'super-negin-saffron-fa'
        prod_super_negin.short_description = 'باکیفیت ترین زعفران دنیا.'
        prod_super_negin.save()

        prod_super_negin.set_current_language('ar')
        prod_super_negin.name = 'زعفران سوبر نقين'
        prod_super_negin.slug = 'super-negin-saffron-ar'
        prod_super_negin.short_description = 'أعلى جودة زعفران في العالم.'
        prod_super_negin.save()

        prod_super_negin.set_current_language('tr')
        prod_super_negin.name = 'Süper Negin Safran'
        prod_super_negin.slug = 'super-negin-safran-tr'
        prod_super_negin.short_description = 'Dünyanın en kaliteli safranı.'
        prod_super_negin.save()

        ProductVariant.objects.create(product=prod_super_negin, weight='5g', packaging_type='Luxury Box', base_price=15.00, stock=100)
        ProductVariant.objects.create(product=prod_super_negin, weight='10g', packaging_type='Luxury Box', base_price=28.00, stock=100)

        # Sargol Saffron
        prod_sargol = Product.objects.create(category=cat_saffron, sku='PK-SAF-SG-01', is_active=True)
        prod_sargol.set_current_language('en')
        prod_sargol.name = 'Sargol Saffron'
        prod_sargol.slug = 'sargol-saffron'
        prod_sargol.short_description = 'All-red saffron threads.'
        prod_sargol.save()

        prod_sargol.set_current_language('fa')
        prod_sargol.name = 'زعفران سرگل'
        prod_sargol.slug = 'sargol-saffron-fa'
        prod_sargol.short_description = 'رشته های زعفران کاملا قرمز.'
        prod_sargol.save()

        prod_sargol.set_current_language('ar')
        prod_sargol.name = 'زعفران سرقل'
        prod_sargol.slug = 'sargol-saffron-ar'
        prod_sargol.short_description = 'خيوط الزعفران الحمراء بالكامل.'
        prod_sargol.save()

        prod_sargol.set_current_language('tr')
        prod_sargol.name = 'Sargol Safran'
        prod_sargol.slug = 'sargol-safran-tr'
        prod_sargol.short_description = 'Tamamı kırmızı safran iplikleri.'
        prod_sargol.save()

        ProductVariant.objects.create(product=prod_sargol, weight='5g', packaging_type='Crystal Jar', base_price=12.00, stock=100)
        ProductVariant.objects.create(product=prod_sargol, weight='10g', packaging_type='Crystal Jar', base_price=22.00, stock=100)

        # Akbari Pistachio
        prod_akbari = Product.objects.create(category=cat_pistachio, sku='PK-PST-AK-01', is_active=True)
        prod_akbari.set_current_language('en')
        prod_akbari.name = 'Akbari Pistachio'
        prod_akbari.slug = 'akbari-pistachio'
        prod_akbari.short_description = 'Long, smiling pistachios.'
        prod_akbari.save()

        prod_akbari.set_current_language('fa')
        prod_akbari.name = 'پسته اکبری'
        prod_akbari.slug = 'akbari-pistachio-fa'
        prod_akbari.short_description = 'پسته های خندان و کشیده.'
        prod_akbari.save()

        prod_akbari.set_current_language('ar')
        prod_akbari.name = 'فستق أكبري'
        prod_akbari.slug = 'akbari-pistachio-ar'
        prod_akbari.short_description = 'فستق طويل ومبتسم.'
        prod_akbari.save()

        prod_akbari.set_current_language('tr')
        prod_akbari.name = 'Akbari Fıstığı'
        prod_akbari.slug = 'akbari-fistigi-tr'
        prod_akbari.short_description = 'Uzun, gülen fıstık.'
        prod_akbari.save()

        ProductVariant.objects.create(product=prod_akbari, weight='1kg', packaging_type='Vacuum Bag', base_price=25.00, stock=100)
        ProductVariant.objects.create(product=prod_akbari, weight='5kg', packaging_type='Bulk Box', base_price=120.00, stock=100)

        # Ahmad Aghaei Pistachio
        prod_ahmad = Product.objects.create(category=cat_pistachio, sku='PK-PST-AA-01', is_active=True)
        prod_ahmad.set_current_language('en')
        prod_ahmad.name = 'Ahmad Aghaei Pistachio'
        prod_ahmad.slug = 'ahmad-aghaei-pistachio'
        prod_ahmad.short_description = 'Sweet and flavorful pistachios.'
        prod_ahmad.save()

        prod_ahmad.set_current_language('fa')
        prod_ahmad.name = 'پسته احمد آقایی'
        prod_ahmad.slug = 'ahmad-aghaei-pistachio-fa'
        prod_ahmad.short_description = 'پسته های شیرین و خوش طعم.'
        prod_ahmad.save()

        prod_ahmad.set_current_language('ar')
        prod_ahmad.name = 'فستق احمد أغايي'
        prod_ahmad.slug = 'ahmad-aghaei-pistachio-ar'
        prod_ahmad.short_description = 'فستق حلو ولذيذ.'
        prod_ahmad.save()

        prod_ahmad.set_current_language('tr')
        prod_ahmad.name = 'Ahmad Aghaei Fıstığı'
        prod_ahmad.slug = 'ahmad-aghaei-fistigi-tr'
        prod_ahmad.short_description = 'Tatlı ve lezzetli fıstık.'
        prod_ahmad.save()

        ProductVariant.objects.create(product=prod_ahmad, weight='1kg', packaging_type='Vacuum Bag', base_price=22.00, stock=100)
        ProductVariant.objects.create(product=prod_ahmad, weight='5kg', packaging_type='Bulk Box', base_price=105.00, stock=100)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))
