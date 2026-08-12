import os
from decimal import Decimal

import django
from django.db import transaction
from django.utils import timezone

# تنظیم صحیح مسیر settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from catalog.models import (
    Category, QualityGrade, PackagingType,
    Product, ProductVariant, TieredPrice
)

# ============================================================
# DATA DEFINITIONS
# ============================================================

CATEGORIES = [
    {
        'slug_en': 'saffron',
        'is_active': True,
        'translations': {
            'fa': {'name': 'زعفران', 'slug': 'زعفران', 'description': 'زعفران ایرانی، مرغوب‌ترین زعفران جهان'},
            'en': {'name': 'Saffron', 'slug': 'saffron', 'description': 'Iranian Saffron, the finest in the world'},
            'ar': {'name': 'الزعفران', 'slug': 'alzafaran', 'description': 'الزعفران الإيراني، الأفضل في العالم'},
            'tr': {'name': 'Safran', 'slug': 'safran-tur', 'description': 'İran Safranı, dünyanın en iyisi'},
        }
    },
    {
        'slug_en': 'pistachio',
        'is_active': True,
        'translations': {
            'fa': {'name': 'پسته', 'slug': 'پسته', 'description': 'پسته ایرانی، با کیفیت عالی برای صادرات'},
            'en': {'name': 'Pistachio', 'slug': 'pistachio', 'description': 'Iranian Pistachio, premium quality for export'},
            'ar': {'name': 'الفستق', 'slug': 'alfustuq', 'description': 'الفستق الإيراني، جودة ممتازة للتصدير'},
            'tr': {'name': 'Antep Fıstığı', 'slug': 'antep-fistigi', 'description': 'İran Antep Fıstığı, ihracat için kaliteli'},
        }
    },
    {
        'slug_en': 'pistachio-kernel',
        'is_active': True,
        'translations': {
            'fa': {'name': 'مغز پسته', 'slug': 'مغز-پسته', 'description': 'مغز پسته ایرانی، پوست‌گیری شده و مرغوب'},
            'en': {'name': 'Pistachio Kernel', 'slug': 'pistachio-kernel', 'description': 'Iranian Pistachio Kernels, shelled and premium'},
            'ar': {'name': 'لب الفستق', 'slug': 'lubb-al-fustuq', 'description': 'لب الفستق الإيراني، مقشر وممتاز'},
            'tr': {'name': 'İç Antep Fıstığı', 'slug': 'ic-antep-fistigi', 'description': 'İran İç Antep Fıstığı, kabuksuz ve kaliteli'},
        }
    },
]

QUALITY_GRADES = [
    {
        'name_en': 'Super Premium',
        'name_fa': 'سوپر پریمیوم',
        'name_ar': 'سوبر بريميوم',
        'name_tr': 'Süper Premium',
    },
    {
        'name_en': 'Premium',
        'name_fa': 'پریمیوم',
        'name_ar': 'بريميوم',
        'name_tr': 'Premium',
    },
    {
        'name_en': 'Export Grade',
        'name_fa': 'درجه صادراتی',
        'name_ar': 'درجة تصدير',
        'name_tr': 'İhracat Kalitesi',
    },
    {
        'name_en': 'Grade A',
        'name_fa': 'درجه A',
        'name_ar': 'الدرجة A',
        'name_tr': 'A Sınıfı',
    },
]

# وزن‌ها به صورت Decimal برای دقت
PACKAGING_TYPES = [
    {
        'weight': Decimal('0.5'),
        'translations': {
            'fa': '۰.۵ گرم', 'en': '0.5 g', 'ar': '۰.۵ غرام', 'tr': '0.5 g'
        }
    },
    {
        'weight': Decimal('1'),
        'translations': {
            'fa': '۱ گرم', 'en': '1 g', 'ar': '۱ غرام', 'tr': '1 g'
        }
    },
    {
        'weight': Decimal('2'),
        'translations': {
            'fa': '۲ گرم', 'en': '2 g', 'ar': '۲ غرام', 'tr': '2 g'
        }
    },
    {
        'weight': Decimal('4.608'),
        'translations': {
            'fa': '۴.۶۰۸ گرم (مثقال)', 'en': '4.608 g (Mesghal)', 'ar': '٤.٦٠٨ غرام (مثقال)', 'tr': '4.608 g (Mesghal)'
        }
    },
    {
        'weight': Decimal('250'),
        'translations': {
            'fa': '۲۵۰ گرم', 'en': '250 g', 'ar': '۲۵۰ غرام', 'tr': '250 g'
        }
    },
    {
        'weight': Decimal('500'),
        'translations': {
            'fa': '۵۰۰ گرم', 'en': '500 g', 'ar': '۵۰۰ غرام', 'tr': '500 g'
        }
    },
    {
        'weight': Decimal('1000'),
        'translations': {
            'fa': '۱ کیلوگرم', 'en': '1 kg', 'ar': '۱ كيلوغرام', 'tr': '1 kg'
        }
    },
    {
        'weight': Decimal('5000'),
        'translations': {
            'fa': '۵ کیلوگرم', 'en': '5 kg', 'ar': '۵ كيلوغرام', 'tr': '5 kg'
        }
    },
    {
        'weight': Decimal('10000'),
        'translations': {
            'fa': '۱۰ کیلوگرم', 'en': '10 kg', 'ar': '۱۰ كيلوغرام', 'tr': '10 kg'
        }
    },
]

# ۱۰ محصول نهایی: ۵ زعفران + ۳ پسته با پوست + ۲ مغز
PRODUCTS_DATA = [
    # ----- زعفران (۵ عدد) -----
    {
        'category_slug': 'saffron',
        'grade_name_en': 'Super Premium',
        'translations': {
            'fa': {
                'name': 'سوپر نگین (اتویی)',
                'slug': 'سوپر-نگین-اتویی',
                'short_description': 'مرغوب‌ترین زعفران، خشک‌شده با دستگاه',
                'full_description': 'زعفران سوپر نگین اتویی از بهترین مزارع خراسان، با عطر و رنگ فوق‌العاده. مناسب برای صادرات و بسته‌بندی‌های لوکس.',
                'seo_title': 'زعفران سوپر نگین اتویی - بهترین کیفیت',
                'meta_description': 'خرید زعفران سوپر نگین اتویی با کیفیت عالی و قیمت مناسب برای صادرات',
            },
            'en': {
                'name': 'Super Negin (Machine Dried)',
                'slug': 'super-negin-machine',
                'short_description': 'Premium saffron, machine-dried for consistency',
                'full_description': 'Super Negin saffron machine-dried to preserve color and aroma. Sourced from the finest farms in Khorasan, ideal for export and premium packaging.',
                'seo_title': 'Super Negin Saffron Machine Dried - Premium Quality',
                'meta_description': 'Buy Super Negin Machine Dried Saffron, high quality export grade.',
            },
            'ar': {
                'name': 'سوبر نيجين (مجفف آلي)',
                'slug': 'سوبر-نيجين-آلي',
                'short_description': 'زعفران ممتاز، مجفف آلياً',
                'full_description': 'زعفران سوبر نيجين المجفف آلياً للحفاظ على اللون والرائحة. مصدر من أفضل مزارع خراسان، مثالي للتصدير والتغليف الفاخر.',
                'seo_title': 'زعفران سوبر نيجين مجفف آلي - جودة ممتازة',
                'meta_description': 'شراء زعفران سوبر نيجين مجفف آلي بجودة عالية للتصدير',
            },
            'tr': {
                'name': 'Süper Negin (Makine Kurutmalı)',
                'slug': 'super-negin-makine',
                'short_description': 'Birinci sınıf safran, makineyle kurutulmuş',
                'full_description': 'Süper Negin safranı, renk ve aroma korumak için makineyle kurutulmuştur. Horasan\'ın en iyi çiftliklerinden temin edilir, ihracat ve lüks ambalaj için idealdir.',
                'seo_title': 'Süper Negin Safran Makine Kurutmalı - Kaliteli',
                'meta_description': 'Süper Negin Makine Kurutmalı Safran satın alın, yüksek kaliteli ihracat sınıfı.',
            }
        },
        'variants': {
            'weights': [Decimal('0.5'), Decimal('1'), Decimal('2'), Decimal('4.608'),
                        Decimal('250'), Decimal('500'), Decimal('1000'), Decimal('5000'), Decimal('10000')],
            'default_weight': Decimal('1'),
            'moq_small': 1,
            'moq_bulk': 5,
        }
    },
    {
        'category_slug': 'saffron',
        'grade_name_en': 'Super Premium',
        'translations': {
            'fa': {
                'name': 'سوپر نگین (دستی)',
                'slug': 'سوپر-نگین-دستی',
                'short_description': 'مرغوب‌ترین زعفران، خشک‌شده به روش سنتی دستی',
                'full_description': 'زعفران سوپر نگین دستی، با دقت و ظرافت چیده و خشک شده. عطر و طعم بی‌نظیر، بهترین انتخاب برای صادرات.',
                'seo_title': 'زعفران سوپر نگین دستی - بهترین کیفیت سنتی',
                'meta_description': 'زعفران سوپر نگین دستی با کیفیت عالی و عطر فوق‌العاده',
            },
            'en': {
                'name': 'Super Negin (Hand Picked)',
                'slug': 'super-negin-hand-picked',
                'short_description': 'Premium saffron, hand-picked and sun-dried',
                'full_description': 'Super Negin hand-picked saffron, traditionally dried for superior aroma and taste. Sourced from the finest farms in Iran.',
                'seo_title': 'Super Negin Hand Picked Saffron - Traditional Quality',
                'meta_description': 'Buy Super Negin Hand Picked Saffron, traditional premium quality.',
            },
            'ar': {
                'name': 'سوبر نيجين (يدوي)',
                'slug': 'سوبر-نيجين-يدوي',
                'short_description': 'زعفران ممتاز، مجفف يدوياً',
                'full_description': 'زعفران سوبر نيجين اليدوي، مجفف تقليدياً للحصول على رائحة وطعم فائقين. مصدر من أفضل مزارع إيران.',
                'seo_title': 'زعفران سوبر نيجين يدوي - جودة تقليدية',
                'meta_description': 'شراء زعفران سوبر نيجين يدوي بجودة تقليدية ممتازة',
            },
            'tr': {
                'name': 'Süper Negin (El İşi)',
                'slug': 'super-negin-el-isi',
                'short_description': 'Birinci sınıf safran, elle toplanmış ve kurutulmuş',
                'full_description': 'Süper Negin elle toplanmış safranı, geleneksel olarak kurutulmuş, üstün aroma ve lezzet için. İran\'ın en iyi çiftliklerinden temin edilir.',
                'seo_title': 'Süper Negin El İşi Safran - Geleneksel Kalite',
                'meta_description': 'Süper Negin El İşi Safran satın alın, geleneksel premium kalite.',
            }
        },
        'variants': {
            'weights': [Decimal('0.5'), Decimal('1'), Decimal('2'), Decimal('4.608'),
                        Decimal('250'), Decimal('500'), Decimal('1000'), Decimal('5000'), Decimal('10000')],
            'default_weight': Decimal('1'),
            'moq_small': 1,
            'moq_bulk': 5,
        }
    },
    {
        'category_slug': 'saffron',
        'grade_name_en': 'Premium',
        'translations': {
            'fa': {
                'name': 'پوشال',
                'slug': 'پوشال',
                'short_description': 'زعفران پوشال با کیفیت بالا',
                'full_description': 'زعفران پوشال، دارای کلاله‌های بلند و عطر قوی. مناسب برای صادرات و مصارف صنعتی.',
                'seo_title': 'زعفران پوشال - کیفیت عالی',
                'meta_description': 'خرید زعفران پوشال با کیفیت بالا و قیمت رقابتی',
            },
            'en': {
                'name': 'Pushal',
                'slug': 'pushal-saffron',
                'short_description': 'High-quality Pushal saffron with long stigmas',
                'full_description': 'Pushal saffron, known for its long stigmas and strong aroma. Ideal for export and industrial use.',
                'seo_title': 'Pushal Saffron - Premium Quality',
                'meta_description': 'Buy Pushal saffron with high quality and competitive price.',
            },
            'ar': {
                'name': 'بوشال',
                'slug': 'pushal',
                'short_description': 'زعفران بوشال عالي الجودة',
                'full_description': 'زعفران بوشال، معروف بطول مياسمه ورائحته القوية. مثالي للتصدير والاستخدام الصناعي.',
                'seo_title': 'زعفران بوشال - جودة ممتازة',
                'meta_description': 'شراء زعفران بوشال بجودة عالية وسعر تنافسي',
            },
            'tr': {
                'name': 'Pushal',
                'slug': 'pushal-safran',
                'short_description': 'Kaliteli Pushal safranı, uzun tepecikli',
                'full_description': 'Pushal safranı, uzun tepecikleri ve güçlü aromasıyla bilinir. İhracat ve endüstriyel kullanım için ideal.',
                'seo_title': 'Pushal Safran - Kaliteli',
                'meta_description': 'Pushal safran satın alın, yüksek kalite ve rekabetçi fiyat.',
            }
        },
        'variants': {
            'weights': [Decimal('0.5'), Decimal('1'), Decimal('2'), Decimal('4.608'),
                        Decimal('250'), Decimal('500'), Decimal('1000'), Decimal('5000'), Decimal('10000')],
            'default_weight': Decimal('1'),
            'moq_small': 1,
            'moq_bulk': 5,
        }
    },
    {
        'category_slug': 'saffron',
        'grade_name_en': 'Premium',
        'translations': {
            'fa': {
                'name': 'دسته',
                'slug': 'دسته-زعفران',
                'short_description': 'زعفران دسته‌بندی شده با کیفیت',
                'full_description': 'زعفران دسته، شامل کلاله‌های مرتب و یکدست. مناسب برای بسته‌بندی‌های لوکس و هدیه.',
                'seo_title': 'زعفران دسته - کیفیت ممتاز',
                'meta_description': 'زعفران دسته با کیفیت بالا و ظاهر عالی برای صادرات',
            },
            'en': {
                'name': 'Bunch',
                'slug': 'bunch-saffron',
                'short_description': 'Bunched saffron with uniform stigmas',
                'full_description': 'Bunch saffron, featuring neatly arranged and uniform stigmas. Perfect for luxury packaging and gifting.',
                'seo_title': 'Bunch Saffron - Premium Quality',
                'meta_description': 'Buy bunch saffron with high quality and excellent appearance for export.',
            },
            'ar': {
                'name': 'عنقود',
                'slug': 'bunch-ar',
                'short_description': 'زعفران عنقودي بمياسم موحدة',
                'full_description': 'زعفران عنقودي، يتميز بمياسم مرتبة وموحدة. مثالي للتغليف الفاخر والهدايا.',
                'seo_title': 'زعفران عنقودي - جودة ممتازة',
                'meta_description': 'شراء زعفران عنقودي بجودة عالية ومظهر ممتاز للتصدير',
            },
            'tr': {
                'name': 'Bunch (Demet)',
                'slug': 'bunch-safran',
                'short_description': 'Demet safran, düzgün tepecikli',
                'full_description': 'Demet safran, düzgün ve tekdüze tepeciklere sahiptir. Lüks ambalaj ve hediye için mükemmel.',
                'seo_title': 'Demet Safran - Kaliteli',
                'meta_description': 'Demet safran satın alın, yüksek kalite ve mükemmel görünüm için ihracat.',
            }
        },
        'variants': {
            'weights': [Decimal('0.5'), Decimal('1'), Decimal('2'), Decimal('4.608'),
                        Decimal('250'), Decimal('500'), Decimal('1000'), Decimal('5000'), Decimal('10000')],
            'default_weight': Decimal('1'),
            'moq_small': 1,
            'moq_bulk': 5,
        }
    },
    {
        'category_slug': 'saffron',
        'grade_name_en': 'Export Grade',
        'translations': {
            'fa': {
                'name': 'خرده ریشه',
                'slug': 'خرده-ریشه',
                'short_description': 'ریشه‌های زعفران با کیفیت صادراتی',
                'full_description': 'خرده ریشه زعفران، قسمت‌های زیرین کلاله که عطر و رنگ خوبی دارند. مناسب برای صادرات و صنایع غذایی.',
                'seo_title': 'خرده ریشه زعفران - کیفیت صادراتی',
                'meta_description': 'خرده ریشه زعفران با کیفیت بالا برای صادرات',
            },
            'en': {
                'name': 'Saffron Root',
                'slug': 'saffron-root',
                'short_description': 'Saffron roots (lower parts) with good aroma',
                'full_description': 'Saffron root, the lower parts of the stigma still containing good aroma and color. Suitable for export and food industry.',
                'seo_title': 'Saffron Root - Export Grade',
                'meta_description': 'Buy saffron root with export quality.',
            },
            'ar': {
                'name': 'جذور الزعفران',
                'slug': 'saffron-root-ar',
                'short_description': 'جذور الزعفران ذات الرائحة الجيدة',
                'full_description': 'جذور الزعفران، الأجزاء السفلية من الميسم التي تحتفظ برائحة ولون جيدين. مناسبة للتصدير والصناعات الغذائية.',
                'seo_title': 'جذور الزعفران - درجة تصدير',
                'meta_description': 'شراء جذور الزعفران بجودة تصدير.',
            },
            'tr': {
                'name': 'Safran Kökü',
                'slug': 'safran-koku',
                'short_description': 'Safran kökü (alt kısımlar) iyi aromalı',
                'full_description': 'Safran kökü, iyi aroma ve renk içeren alt tepecik kısımları. İhracat ve gıda endüstrisi için uygundur.',
                'seo_title': 'Safran Kökü - İhracat Kalitesi',
                'meta_description': 'Safran kökü satın alın, ihracat kalitesinde.',
            }
        },
        'variants': {
            'weights': [Decimal('0.5'), Decimal('1'), Decimal('2'), Decimal('4.608'),
                        Decimal('250'), Decimal('500'), Decimal('1000'), Decimal('5000'), Decimal('10000')],
            'default_weight': Decimal('1'),
            'moq_small': 1,
            'moq_bulk': 5,
        }
    },

    # ----- پسته با پوست (۳ عدد) -----
    {
        'category_slug': 'pistachio',
        'grade_name_en': 'Premium',
        'translations': {
            'fa': {
                'name': 'فندقی',
                'slug': 'فندقی',
                'short_description': 'پسته فندقی مرغوب صادراتی',
                'full_description': 'پسته فندقی با پوست نازک و طعم عالی. مناسب برای صادرات و بازارهای بین‌المللی.',
                'seo_title': 'پسته فندقی - مرغوب و صادراتی',
                'meta_description': 'خرید پسته فندقی با کیفیت بالا و قیمت مناسب',
            },
            'en': {
                'name': 'Fandoghi Pistachio',
                'slug': 'fandoghi-pistachio',
                'short_description': 'Premium Fandoghi pistachio for export',
                'full_description': 'Fandoghi pistachio with thin shell and excellent taste. Ideal for export and international markets.',
                'seo_title': 'Fandoghi Pistachio - Premium Export Quality',
                'meta_description': 'Buy Fandoghi pistachio with high quality and competitive price.',
            },
            'ar': {
                'name': 'فستق فندقي',
                'slug': 'fandoghi-ar',
                'short_description': 'فستق فندقي ممتاز للتصدير',
                'full_description': 'فستق فندقي بقشرة رقيقة وطعم ممتاز. مثالي للتصدير والأسواق الدولية.',
                'seo_title': 'فستق فندقي - جودة تصدير ممتازة',
                'meta_description': 'شراء فستق فندقي بجودة عالية وسعر تنافسي',
            },
            'tr': {
                'name': 'Fandoghi Antep Fıstığı',
                'slug': 'fandoghi-antep',
                'short_description': 'Kaliteli Fandoghi Antep fıstığı ihracat için',
                'full_description': 'Fandoghi Antep fıstığı, ince kabuklu ve mükemmel lezzetli. İhracat ve uluslararası pazarlar için ideal.',
                'seo_title': 'Fandoghi Antep Fıstığı - Premium İhracat Kalitesi',
                'meta_description': 'Fandoghi Antep fıstığı satın alın, yüksek kalite ve rekabetçi fiyat.',
            }
        },
        'variants': {
            'weights': [Decimal('250'), Decimal('500'), Decimal('1000'), Decimal('5000'), Decimal('10000')],
            'default_weight': Decimal('1000'),
            'moq_small': 1,
            'moq_bulk': 5,
        }
    },
    {
        'category_slug': 'pistachio',
        'grade_name_en': 'Premium',
        'translations': {
            'fa': {
                'name': 'اکبری',
                'slug': 'اکبری',
                'short_description': 'پسته اکبری درجه یک',
                'full_description': 'پسته اکبری با دانه‌های درشت و طعم بی‌نظیر. یکی از بهترین ارقام برای صادرات.',
                'seo_title': 'پسته اکبری - مرغوب و درشت',
                'meta_description': 'خرید پسته اکبری با کیفیت عالی و دانه‌های درشت',
            },
            'en': {
                'name': 'Akbari Pistachio',
                'slug': 'akbari-pistachio',
                'short_description': 'Premium Akbari pistachio with large kernels',
                'full_description': 'Akbari pistachio with large, elongated kernels and exceptional taste. One of the best varieties for export.',
                'seo_title': 'Akbari Pistachio - Premium Large Kernels',
                'meta_description': 'Buy Akbari pistachio with high quality and large kernels.',
            },
            'ar': {
                'name': 'فستق أكبري',
                'slug': 'akbari-ar',
                'short_description': 'فستق أكبري ممتاز بحبات كبيرة',
                'full_description': 'فستق أكبري بحبات كبيرة ممدودة وطعم استثنائي. واحد من أفضل الأصناف للتصدير.',
                'seo_title': 'فستق أكبري - حبات كبيرة ممتازة',
                'meta_description': 'شراء فستق أكبري بجودة عالية وحبات كبيرة.',
            },
            'tr': {
                'name': 'Akbari Antep Fıstığı',
                'slug': 'akbari-antep',
                'short_description': 'Kaliteli Akbari Antep fıstığı, büyük iç',
                'full_description': 'Akbari Antep fıstığı, büyük ve uzun içleriyle olağanüstü lezzetli. İhracat için en iyi çeşitlerden biri.',
                'seo_title': 'Akbari Antep Fıstığı - Büyük İç Kalite',
                'meta_description': 'Akbari Antep fıstığı satın alın, yüksek kalite ve büyük iç.',
            }
        },
        'variants': {
            'weights': [Decimal('250'), Decimal('500'), Decimal('1000'), Decimal('5000'), Decimal('10000')],
            'default_weight': Decimal('1000'),
            'moq_small': 1,
            'moq_bulk': 5,
        }
    },
    {
        'category_slug': 'pistachio',
        'grade_name_en': 'Premium',
        'translations': {
            'fa': {
                'name': 'احمد آقایی',
                'slug': 'احمد-آقایی',
                'short_description': 'پسته احمد آقایی مرغوب',
                'full_description': 'پسته احمد آقایی با پوست باز و دانه‌های کشیده. طعم لذیذ و کیفیت بالا، مناسب صادرات.',
                'seo_title': 'پسته احمد آقایی - کیفیت بالا',
                'meta_description': 'خرید پسته احمد آقایی با کیفیت عالی و طعم بی‌نظیر',
            },
            'en': {
                'name': 'Ahmad Aghaei Pistachio',
                'slug': 'ahmad-aghaee-pistachio',
                'short_description': 'Premium Ahmad Aghaei pistachio with open shells',
                'full_description': 'Ahmad Aghaei pistachio with open shells and elongated kernels. Delicious taste and high quality, perfect for export.',
                'seo_title': 'Ahmad Aghaei Pistachio - High Quality',
                'meta_description': 'Buy Ahmad Aghaei pistachio with excellent quality and taste.',
            },
            'ar': {
                'name': 'فستق أحمد آقائي',
                'slug': 'ahmad-aghaee-ar',
                'short_description': 'فستق أحمد آقائي ممتاز بقشور مفتوحة',
                'full_description': 'فستق أحمد آقائي بقشور مفتوحة وحبات ممدودة. طعم لذيذ وجودة عالية، مثالي للتصدير.',
                'seo_title': 'فستق أحمد آقائي - جودة عالية',
                'meta_description': 'شراء فستق أحمد آقائي بجودة ممتازة وطعم رائع.',
            },
            'tr': {
                'name': 'Ahmad Aghaei Antep Fıstığı',
                'slug': 'ahmad-aghaee-antep',
                'short_description': 'Kaliteli Ahmad Aghaei Antep fıstığı, açık kabuklu',
                'full_description': 'Ahmad Aghaei Antep fıstığı, açık kabuklu ve uzun içli. Lezzetli tat ve yüksek kalite, ihracat için mükemmel.',
                'seo_title': 'Ahmad Aghaei Antep Fıstığı - Yüksek Kalite',
                'meta_description': 'Ahmad Aghaei Antep fıstığı satın alın, mükemmel kalite ve tat.',
            }
        },
        'variants': {
            'weights': [Decimal('250'), Decimal('500'), Decimal('1000'), Decimal('5000'), Decimal('10000')],
            'default_weight': Decimal('1000'),
            'moq_small': 1,
            'moq_bulk': 5,
        }
    },

    # ----- مغز پسته (۲ عدد) -----
    {
        'category_slug': 'pistachio-kernel',
        'grade_name_en': 'Export Grade',
        'translations': {
            'fa': {
                'name': 'مغز کله قوچی',
                'slug': 'مغز-کله-قوچی',
                'short_description': 'مغز پسته کله قوچی صادراتی',
                'full_description': 'مغز کله قوچی، پوست‌گیری شده و مرغوب. مناسب برای صادرات و صنایع غذایی.',
                'seo_title': 'مغز کله قوچی - کیفیت صادراتی',
                'meta_description': 'خرید مغز کله قوچی با کیفیت بالا برای صادرات',
            },
            'en': {
                'name': 'Kalleh Ghouchi Kernel',
                'slug': 'kalleh-ghouchi-kernel',
                'short_description': 'Shelled Kalleh Ghouchi pistachio kernels',
                'full_description': 'Kalleh Ghouchi kernels, shelled and premium quality. Ideal for export and food processing.',
                'seo_title': 'Kalleh Ghouchi Kernel - Export Quality',
                'meta_description': 'Buy Kalleh Ghouchi kernels with high quality for export.',
            },
            'ar': {
                'name': 'لب كله قوچي',
                'slug': 'kalleh-ghouchi-kernel-ar',
                'short_description': 'لب فستق كله قوچي مقشر',
                'full_description': 'لب كله قوچي، مقشر وجودة ممتازة. مثالي للتصدير وتصنيع الأغذية.',
                'seo_title': 'لب كله قوچي - جودة تصدير',
                'meta_description': 'شراء لب كله قوچي بجودة عالية للتصدير.',
            },
            'tr': {
                'name': 'Kalleh Ghouchi İçi',
                'slug': 'kalleh-ghouchi-ici',
                'short_description': 'Kabuksuz Kalleh Ghouchi Antep fıstığı içi',
                'full_description': 'Kalleh Ghouchi içi, kabuksuz ve kaliteli. İhracat ve gıda işleme için ideal.',
                'seo_title': 'Kalleh Ghouchi İçi - İhracat Kalitesi',
                'meta_description': 'Kalleh Ghouchi içi satın alın, yüksek kalite ihracat.',
            }
        },
        'variants': {
            'weights': [Decimal('250'), Decimal('500'), Decimal('1000'), Decimal('5000'), Decimal('10000')],
            'default_weight': Decimal('1000'),
            'moq_small': 1,
            'moq_bulk': 5,
        }
    },
    {
        'category_slug': 'pistachio-kernel',
        'grade_name_en': 'Export Grade',
        'translations': {
            'fa': {
                'name': 'مغز احمد آقایی',
                'slug': 'مغز-احمد-آقایی',
                'short_description': 'مغز پسته احمد آقایی صادراتی',
                'full_description': 'مغز احمد آقایی، پوست‌گیری شده و با کیفیت عالی. مناسب برای صادرات و مصارف صنعتی.',
                'seo_title': 'مغز احمد آقایی - کیفیت بالا',
                'meta_description': 'خرید مغز احمد آقایی با کیفیت عالی برای صادرات',
            },
            'en': {
                'name': 'Ahmad Aghaei Kernel',
                'slug': 'ahmad-aghaee-kernel',
                'short_description': 'Shelled Ahmad Aghaei pistachio kernels',
                'full_description': 'Ahmad Aghaei kernels, shelled and high quality. Perfect for export and industrial use.',
                'seo_title': 'Ahmad Aghaei Kernel - High Quality',
                'meta_description': 'Buy Ahmad Aghaei kernels with excellent quality for export.',
            },
            'ar': {
                'name': 'لب أحمد آقائي',
                'slug': 'ahmad-aghaee-kernel-ar',
                'short_description': 'لب فستق أحمد آقائي مقشر',
                'full_description': 'لب أحمد آقائي، مقشر وعالي الجودة. مثالي للتصدير والاستخدام الصناعي.',
                'seo_title': 'لب أحمد آقائي - جودة عالية',
                'meta_description': 'شراء لب أحمد آقائي بجودة ممتازة للتصدير.',
            },
            'tr': {
                'name': 'Ahmad Aghaei İçi',
                'slug': 'ahmad-aghaee-ici',
                'short_description': 'Kabuksuz Ahmad Aghaei Antep fıstığı içi',
                'full_description': 'Ahmad Aghaei içi, kabuksuz ve yüksek kalite. İhracat ve endüstriyel kullanım için mükemmel.',
                'seo_title': 'Ahmad Aghaei İçi - Yüksek Kalite',
                'meta_description': 'Ahmad Aghaei içi satın alın, mükemmel kalite ihracat.',
            }
        },
        'variants': {
            'weights': [Decimal('250'), Decimal('500'), Decimal('1000'), Decimal('5000'), Decimal('10000')],
            'default_weight': Decimal('1000'),
            'moq_small': 1,
            'moq_bulk': 5,
        }
    },
]

# ============================================================
# HELPER FUNCTIONS (اصلاح‌شده برای Decimal)
# ============================================================

def get_or_create_category(data):
    slug_en = data['slug_en']
    existing = Category.objects.filter(translations__slug=slug_en, translations__language_code='en').first()
    if existing:
        for lang, trans in data['translations'].items():
            existing.translations.update_or_create(
                language_code=lang,
                defaults=trans
            )
        existing.is_active = data.get('is_active', True)
        existing.save()
        return existing
    else:
        obj = Category(is_active=data.get('is_active', True))
        obj.save()
        for lang, trans in data['translations'].items():
            obj.translations.create(language_code=lang, **trans)
        return obj

def get_or_create_quality_grade(name_translations):
    en_name = name_translations['en']
    existing = QualityGrade.objects.filter(translations__name=en_name, translations__language_code='en').first()
    if existing:
        for lang, name in name_translations.items():
            existing.translations.update_or_create(
                language_code=lang,
                defaults={'name': name}
            )
        return existing
    else:
        obj = QualityGrade()
        obj.save()
        for lang, name in name_translations.items():
            obj.translations.create(language_code=lang, name=name)
        return obj

def get_or_create_packaging_type(weight, translations):
    en_name = translations['en']
    existing = PackagingType.objects.filter(translations__name=en_name, translations__language_code='en').first()
    if existing:
        for lang, name in translations.items():
            existing.translations.update_or_create(
                language_code=lang,
                defaults={'name': name}
            )
        return existing
    else:
        obj = PackagingType()
        obj.save()
        for lang, name in translations.items():
            obj.translations.create(language_code=lang, name=name)
        return obj

def get_or_create_product(product_data):
    slug_en = product_data['translations']['en']['slug']
    existing = Product.objects.filter(translations__slug=slug_en, translations__language_code='en').first()
    if existing:
        for lang, trans in product_data['translations'].items():
            existing.translations.update_or_create(
                language_code=lang,
                defaults=trans
            )
        existing.is_active = True
        existing.published_at = timezone.now()
        category = Category.objects.filter(translations__slug=product_data['category_slug'], translations__language_code='en').first()
        if category:
            existing.category = category
        grade = QualityGrade.objects.filter(translations__name=product_data['grade_name_en'], translations__language_code='en').first()
        if grade:
            existing.grade = grade
        existing.save()
        return existing
    else:
        obj = Product(is_active=True, published_at=timezone.now())
        category = Category.objects.filter(translations__slug=product_data['category_slug'], translations__language_code='en').first()
        if category:
            obj.category = category
        grade = QualityGrade.objects.filter(translations__name=product_data['grade_name_en'], translations__language_code='en').first()
        if grade:
            obj.grade = grade
        obj.save()
        for lang, trans in product_data['translations'].items():
            obj.translations.create(language_code=lang, **trans)
        return obj

def create_variant(product, packaging_type, weight, sku, moq, is_default):
    variant, created = ProductVariant.objects.get_or_create(
        product=product,
        packaging_type=packaging_type,
        weight_in_grams=weight,   # حالا DecimalField قبول می‌کند
        defaults={
            'sku': sku,
            'moq': moq,
            'is_default': is_default,
        }
    )
    if not created:
        variant.sku = sku
        variant.moq = moq
        variant.is_default = is_default
        variant.save()
    return variant

def create_tiered_prices(variant, price_tiers):
    for tier in price_tiers:
        TieredPrice.objects.update_or_create(
            product_variant=variant,
            min_qty=tier['min'],
            max_qty=tier.get('max'),
            defaults={'price_usd': tier['price']}
        )

# ============================================================
# PRICE GENERATION HELPERS (با Decimal)
# ============================================================

def get_base_price_per_gram(product_name, grade, category_slug):
    if category_slug == 'saffron':
        if 'Super Negin' in product_name:
            return Decimal('12.00') if 'Hand' in product_name else Decimal('10.00')
        elif 'Pushal' in product_name:
            return Decimal('8.00')
        elif 'Bunch' in product_name:
            return Decimal('7.50')
        elif 'Saffron Root' in product_name:
            return Decimal('5.00')
        else:
            return Decimal('6.00')
    elif category_slug == 'pistachio':
        base_per_kg = Decimal('15.00')
        if 'Akbari' in product_name:
            base_per_kg = Decimal('18.00')
        elif 'Ahmad' in product_name:
            base_per_kg = Decimal('17.00')
        elif 'Kalleh' in product_name:
            base_per_kg = Decimal('16.00')
        else:
            base_per_kg = Decimal('14.00')
        return base_per_kg / Decimal('1000')
    else:  # kernel
        base_per_kg = Decimal('20.00')
        if 'Kalleh' in product_name:
            base_per_kg = Decimal('22.00')
        elif 'Ahmad' in product_name:
            base_per_kg = Decimal('21.00')
        elif 'Almond' in product_name:
            base_per_kg = Decimal('19.00')
        elif 'Kalak' in product_name:
            base_per_kg = Decimal('20.00')
        return base_per_kg / Decimal('1000')

def generate_price_tiers(weight, base_price_per_gram, is_retail):
    unit_price = base_price_per_gram * weight
    if is_retail:
        markup = Decimal('1.5')
        price = unit_price * markup
        tiers = [
            {'min': 1, 'max': 10, 'price': price},
            {'min': 11, 'max': 50, 'price': price * Decimal('0.95')},
            {'min': 51, 'max': 200, 'price': price * Decimal('0.90')},
            {'min': 201, 'max': None, 'price': price * Decimal('0.85')},
        ]
    else:
        price = unit_price * Decimal('1.1')
        tiers = [
            {'min': 1, 'max': 5, 'price': price},
            {'min': 6, 'max': 20, 'price': price * Decimal('0.95')},
            {'min': 21, 'max': 100, 'price': price * Decimal('0.90')},
            {'min': 101, 'max': None, 'price': price * Decimal('0.85')},
        ]
    for tier in tiers:
        tier['price'] = tier['price'].quantize(Decimal('0.01'))
    return tiers

# ============================================================
# MAIN SEED FUNCTION
# ============================================================

def seed():
    print("Starting product data seeding (10 products)...")

    with transaction.atomic():
        # 1. Categories
        print("Creating categories...")
        category_map = {}
        for cat_data in CATEGORIES:
            cat = get_or_create_category(cat_data)
            category_map[cat_data['slug_en']] = cat
        print("Categories created/updated.")

        # 2. Quality grades
        print("Creating quality grades...")
        grade_map = {}
        for grade in QUALITY_GRADES:
            name_trans = {'en': grade['name_en'], 'fa': grade['name_fa'],
                          'ar': grade['name_ar'], 'tr': grade['name_tr']}
            g = get_or_create_quality_grade(name_trans)
            grade_map[grade['name_en']] = g
        print("Quality grades created/updated.")

        # 3. Packaging types
        print("Creating packaging types...")
        packaging_map = {}  # Decimal weight -> object
        for pkg in PACKAGING_TYPES:
            p = get_or_create_packaging_type(pkg['weight'], pkg['translations'])
            packaging_map[pkg['weight']] = p
        print("Packaging types created/updated.")

        # 4. Products (دقیقاً ۱۰ عدد)
        print("Creating products (10 exactly)...")
        products = []
        for prod_data in PRODUCTS_DATA:
            product = get_or_create_product(prod_data)
            products.append((product, prod_data))
        print(f"Total products prepared: {len(products)}")

        # 5. Variants and prices
        print("Creating variants and tiered prices...")
        sku_counter = 1
        for product, prod_data in products:
            category_slug = prod_data['category_slug']
            variants_info = prod_data['variants']
            weights = variants_info['weights']
            default_weight = variants_info['default_weight']
            moq_small = variants_info['moq_small']
            moq_bulk = variants_info['moq_bulk']

            product_name = prod_data['translations']['en']['name']
            grade_name = prod_data['grade_name_en']
            base_price_per_gram = get_base_price_per_gram(product_name, grade_name, category_slug)

            # تعیین کد محصول برای SKU
            if category_slug == 'saffron':
                if 'Super Negin' in product_name:
                    prod_code = 'SNM' if 'Machine' in product_name else 'SNH'
                elif 'Pushal' in product_name:
                    prod_code = 'PSH'
                elif 'Bunch' in product_name:
                    prod_code = 'BUN'
                elif 'Root' in product_name:
                    prod_code = 'ROT'
                else:
                    prod_code = 'SAF'
            elif category_slug == 'pistachio':
                if 'Fandoghi' in product_name:
                    prod_code = 'FAN'
                elif 'Akbari' in product_name:
                    prod_code = 'AKB'
                elif 'Ahmad' in product_name:
                    prod_code = 'AHA'
                else:
                    prod_code = 'PIS'
            else:  # kernel
                if 'Kalleh' in product_name:
                    prod_code = 'KAL'
                elif 'Ahmad' in product_name:
                    prod_code = 'AHA'
                elif 'Almond' in product_name:
                    prod_code = 'ALM'
                elif 'Kalak' in product_name:
                    prod_code = 'KLK'
                else:
                    prod_code = 'KRN'

            for weight in weights:
                is_retail = weight <= Decimal('4.608')
                moq = moq_small if is_retail else moq_bulk
                is_default = (weight == default_weight)
                sku = f"PK-{category_slug[:3].upper()}-{prod_code}-{sku_counter:04d}"
                sku_counter += 1

                packaging_type = packaging_map[weight]
                variant = create_variant(
                    product=product,
                    packaging_type=packaging_type,
                    weight=weight,
                    sku=sku,
                    moq=moq,
                    is_default=is_default
                )
                price_tiers = generate_price_tiers(weight, base_price_per_gram, is_retail)
                create_tiered_prices(variant, price_tiers)

                print(f"  Variant: {product} - {weight}g, SKU: {sku}")

        print("All 10 products with variants and prices created successfully!")


if __name__ == "__main__":
    seed()