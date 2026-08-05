import os
import polib

LOCALE_DIR = 'locale'

# دیکشنری جامع ترجمه‌های فوتر و هدر سایت
TRANSLATIONS = {
    "Get in Touch": {
        "fa": "در ارتباط باشید",
        "ar": "ابق على تواصل",
        "tr": "İletişimde Kalın"
    },
    "Newsletter": {
        "fa": "خبرنامه",
        "ar": "النشرة الإخبارية",
        "tr": "Bülten"
    },
    "Subscribe to our newsletter to get the latest updates and luxury offers.": {
        "fa": "برای دریافت آخرین به‌روزرسانی‌ها و پیشنهادات ویژه ما، در خبرنامه مشترک شوید.",
        "ar": "اشترك في النشرة الإخبارية للحصول على أحدث التحديثات والعروض الفاخرة.",
        "tr": "En son güncellemeleri ve lüks teklifleri almak için bültenimize abone olun."
    },
    "Success!": {
        "fa": "موفقیت!",
        "ar": "نجاح!",
        "tr": "Başarılı!"
    },
    "You have been added to our email list.": {
        "fa": "شما به لیست ایمیل ما اضافه شدید.",
        "ar": "تمت إضافتك إلى قائمة البريد الإلكتروني لدينا.",
        "tr": "E-posta listemize eklendiniz."
    },
    "Email Address": {
        "fa": "آدرس ایمیل",
        "ar": "عنوان البريد الإلكتروني",
        "tr": "E-posta Adresi"
    },
    "Subscribe": {
        "fa": "عضویت در خبرنامه",
        "ar": "اشتراك",
        "tr": "Abone Ol"
    },
    "About Us": {
        "fa": "درباره ما",
        "ar": "معلومات عنا",
        "tr": "Hakkımızda"
    },
    "Hossein Karimi Trading - Supplying the finest Iranian Saffron and Pistachio.": {
        "fa": "بازرگانی حسین کریمی - تأمین‌کننده بهترین زعفران و پسته ایرانی.",
        "ar": "تجارة حسين كريمي - المورّد لأفضل الزعفران والفستق الإيراني.",
        "tr": "Hossein Karimi Ticaret - En kaliteli İran safranı ve Antep fıstığının tedarikçisi."
    },
    "Contact Us": {
        "fa": "تماس با ما",
        "ar": "اتصل بنا",
        "tr": "İletişim"
    },
    "Corner of Chamran 28, Chamran St., Sabzevar, Khorasan Razavi, Iran": {
        "fa": "ایران، خراسان رضوی، سبزوار، خیابان چمران، نبش چمران ۲۸",
        "ar": "إيران، خراسان الرضوية، سبزوار، شارع جمران، زاوية جمران 28",
        "tr": "İran, Razavi Horasan, Sabzevar, Çamran Caddesi, Çamran 28 Köşesi"
    },
    "Follow Us": {
        "fa": "ما را دنبال کنید",
        "ar": "تابعنا",
        "tr": "Bizi Takip Edin"
    },
    "Palace Karimi Logo": {
        "fa": "لوگوی پالاس کریمی",
        "ar": "شعار بالاس كريمي",
        "tr": "Palace Karimi Logosu"
    },
    "© 2026 Palace Karimi. All Rights Reserved.": {
        "fa": "© ۲۰۲۶ پالاس کریمی. تمامی حقوق محفوظ است.",
        "ar": "© 2026 Palace Karimi. جميع الحقوق محفوظة.",
        "tr": "© 2026 Palace Karimi. Tüm Hakları Saklıdır."
    },
    "Designed & Developed by": {
        "fa": "طراحی و توسعه توسط",
        "ar": "تصميم وتطوير بواسطة",
        "tr": "Tasarım ve Geliştirme:"
    },
    "FAQ": {
        "fa": "سوالات متداول",
        "ar": "أسئلة مكررة",
        "tr": "SSS"
    },
    "Sitemap": {
        "fa": "نقشه سایت",
        "ar": "خريطة الموقع",
        "tr": "Site Haritası"
    },
    "Palace Karimi | Luxury Persian Saffron & Pistachio": {
        "fa": "پالاس کریمی | زعفران و پسته لوکس ایرانی",
        "ar": "بالاس كريمي | الزعفران والفستق الإيراني الفاخر",
        "tr": "Palace Karimi | Lüks İran Safranı ve Şam Fıstığı"
    },
    "In God We Trust...": {
        "fa": "به خدا توکل داریم...",
        "ar": "في الله نثق...",
        "tr": "Tanrı'ya Güveniyoruz..."
    },
    "Working Hours:": {
        "fa": "ساعات کاری:",
        "ar": "ساعات العمل:",
        "tr": "Çalışma Saatleri:"
    },

    "08:00 - 20:00": {
        "fa": "۰۸:۰۰ - ۲۰:۰۰",
        "ar": "08:00 - 20:00",
        "tr": "08:00 - 20:00"
    },

    "0992 759 0575": {
        "fa": "۰۹۹۲ ۷۵۹ ۰۵۷۵",
        "ar": "0992 759 0575",
        "tr": "0992 759 0575"
    },

    "0930 375 5667": {
        "fa": "۰۹۳۰ ۳۷۵ ۵۶۶۷",
        "ar": "0930 375 5667",
        "tr": "0930 375 5667"
    },

    "051 44 29 20 21": {
        "fa": "۰۵۱ ۴۴ ۲۹ ۲۰ ۲۱",
        "ar": "051 44 29 20 21",
        "tr": "051 44 29 20 21"
    },

    "palacekarimi2023@gmail.com": {
        "fa": "palacekarimi2023@gmail.com",
        "ar": "palacekarimi2023@gmail.com",
        "tr": "palacekarimi2023@gmail.com"
    },

    "Instagram": {
        "fa": "اینستاگرام",
        "ar": "إنستغرام",
        "tr": "Instagram"
    },

    "Facebook": {
        "fa": "فیسبوک",
        "ar": "فيسبوك",
        "tr": "Facebook"
    },

    "Twitter": {
        "fa": "توییتر",
        "ar": "إكس (تويتر)",
        "tr": "X (Twitter)"
    },

    "Linkedin": {
        "fa": "لینکدین",
        "ar": "لينكدإن",
        "tr": "LinkedIn"
    },
"Our": {
        "fa": "دفتر",
        "ar": "مكتبنا",
        "tr": "Ofisimiz"
    },
    "Office": {
        "fa": "ما",
        "ar": "",
        "tr": ""
    },
    "Address:": {
        "fa": "آدرس:",
        "ar": "العنوان:",
        "tr": "Adres:"
    },
    "Phone:": {
        "fa": "تلفن:",
        "ar": "هاتف:",
        "tr": "Telefon:"
    },
    "Email:": {
        "fa": "ایمیل:",
        "ar": "البريد الإلكتروني:",
        "tr": "E-posta:"
    },
    "Business": {
        "fa": "ساعت",
        "ar": "ساعات",
        "tr": "Çalışma"
    },
    "Hours": {
        "fa": "کاری",
        "ar": "العمل",
        "tr": "Saatleri"
    },
    "Everyday - 08:00 to 20:00": {
        "fa": "همه‌روزه - ۰۸:۰۰ صبح تا ۲۰:۰۰ شب",
        "ar": "كل يوم - 08:00 إلى 20:00",
        "tr": "Her gün - 08:00 ile 20:00 arası"
    },
    "Admin Panel": {
            "fa": "پنل مدیریت",
            "ar": "لوحة الإدارة",
            "tr": "Yönetici Paneli"
        },
    "Palace Karimi: From the heart of orchards to the heart of business": {
        "en": "Palace Karimi: From the heart of orchards to the heart of business",
        "fa": "پالس کریمی؛ از دل باغستان تا قلب تجارت",
        "ar": "بالس كريمي؛ من قلب البساتين إلى قلب التجارة",
        "tr": "Palace Karimi; Meyve bahçelerinin kalbinden ticaretin kalbine"
    },

    "Premium Quality": {
        "en": "Premium Quality",
        "fa": "کیفیت ممتاز",
        "ar": "جودة ممتازة",
        "tr": "Üstün Kalite"
    },

    "Handpicked from the finest orchards and processed under strict quality standards.": {
        "en": "Handpicked from the finest orchards and processed under strict quality standards.",
        "fa": "دست‌چین شده از بهترین باغ‌ها و فرآوری شده تحت دقیق‌ترین استانداردهای کیفی.",
        "ar": "مقطوفة بعناية من أفضل البساتين ومعالجة وفقاً لأدق معايير الجودة.",
        "tr": "En iyi bahçelerden özenle seçilmiş ve sıkı kalite standartlarında işlenmiştir."
    },
    "Terms & FAQ": {
            "en": "Terms & FAQ",
            "fa": "قوانین و سوالات متداول",
            "ar": "الشروط والأسئلة الشائعة",
            "tr": "Şartlar ve SSS"
        },
    "Competitive Pricing": {
        "en": "Competitive Pricing",
        "fa": "قیمت‌های رقابتی",
        "ar": "أسعار تنافسية",
        "tr": "Rekabetçi Fiyatlandırma"
    },

    "Direct sourcing allows us to offer the best market prices for B2B partners.": {
        "en": "Direct sourcing allows us to offer the best market prices for B2B partners.",
        "fa": "تامین مستقیم به ما اجازه می‌دهد بهترین قیمت‌های بازار را به شرکای B2B خود ارائه دهیم.",
        "ar": "يتيح لنا التوريد المباشر تقديم أفضل أسعار السوق لشركائنا التجاريين.",
        "tr": "Doğrudan tedarik, B2B ortaklarımız için en iyi piyasa fiyatlarını sunmamızı sağlar."
    },
    "Every great success starts with a small decision and years of relentless effort.": {
        "en": "Every great success starts with a small decision and years of relentless effort.",
        "fa": "هر موفقیت بزرگی، از یک تصمیم کوچک و سال‌ها تلاش بی‌وقفه آغاز می‌شود.",
        "ar": "كل نجاح عظيم يبدأ بقرار صغير وسنوات من الجهد الدؤوب.",
        "tr": "Her büyük başarı, küçük bir kararla ve yıllar süren amansız bir çabayla başlar."
    },
    "The Roots": {
        "en": "The Roots",
        "fa": "ریشه‌ها",
        "ar": "الجذور",
        "tr": "Kökler"
    },
    "Early Ambitions": {
        "en": "Early Ambitions",
        "fa": "اهداف اولیه و تجربیات",
        "ar": "الطموحات المبكرة",
        "tr": "Erken Hedefler"
    },
    "Hossein Karimi’s entrepreneurial journey began at age 16 by managing a poultry farm, followed by establishing a charcoal factory at 19. These early years built the strong foundation of leadership and market expertise.": {
        "en": "Hossein Karimi’s entrepreneurial journey began at age 16 by managing a poultry farm, followed by establishing a charcoal factory at 19. These early years built the strong foundation of leadership and market expertise.",
        "fa": "مسیر کارآفرینی حسین کریمی در ۱۶ سالگی با اداره یک مرغداری آغاز شد و در ۱۹ سالگی با تأسیس کارخانه تولید زغال ادامه یافت. این سال‌ها پایه‌های محکم رهبری و شناخت بازار را در او شکل داد.",
        "ar": "بدأت رحلة حسين كريمي في ريادة الأعمال في سن الـ ۱۶ من خلال إدارة مزرعة دواجن، وتلاها إنشاء مصنع للفحم في سن الـ ۱۹. بنت هذه السنوات الأولى أساساً قوياً للقيادة والخبرة في السوق.",
        "tr": "Hossein Karimi'nin girişimcilik yolculuğu 16 yaşında bir tavuk çiftliğini yöneterek başladı ve 19 yaşında bir kömür fabrikası kurmasıyla devam etti. Bu ilk yıllar, liderlik ve pazar uzmanlığının güçlü temelini oluşturdu."
    },
    "2019": {
        "en": "2019",
        "fa": "۱۳۹۸",
        "ar": "۲۰۱۹",
        "tr": "2019"
    },
    "The Birth of Palace Karimi": {
        "en": "The Birth of Palace Karimi",
        "fa": "تولد پالِس کریمی",
        "ar": "ولادة بالس كريمي",
        "tr": "Palace Karimi'nin Doğuşu"
    },
    "Starting with a small capital of just 10 million Tomans, Hossein and his wife began their pistachio business. Products were lovingly sorted at home at night and distributed to local confectioneries during the day.": {
        "en": "Starting with a small capital of just 10 million Tomans, Hossein and his wife began their pistachio business. Products were lovingly sorted at home at night and distributed to local confectioneries during the day.",
        "fa": "حسین کریمی و همسرش تنها با ۱۰ میلیون تومان سرمایه وارد حوزه پسته شدند. شب‌ها پسته‌ها را در خانه پاک می‌کردند و صبح‌ها برای فروش به قنادی‌های محلی می‌بردند.",
        "ar": "بدأ حسين وزوجته تجارة الفستق برأس مال صغير بلغ ۱۰ ملايين تومان فقط. كانت المنتجات تُفرز بحب في المنزل ليلاً وتُوزع على محلات الحلويات المحلية نهاراً.",
        "tr": "Sadece 10 milyon Tümen gibi küçük bir sermaye ile başlayan Hossein ve eşi, fıstık işine girdiler. Ürünler geceleri evde sevgiyle ayıklanıyor ve gündüzleri yerel pastanelere dağıtılıyordu."
    },
    "The Journey": {
        "en": "The Journey",
        "fa": "مسیر پرچالش",
        "ar": "الرحلة",
        "tr": "Yolculuk"
    },
    "The Turning Point": {
        "en": "The Turning Point",
        "fa": "نقطه عطف",
        "ar": "نقطة التحول",
        "tr": "Dönüm Noktası"
    },
    "Joined by Hassan Dolatabadi, the team embarked on a challenging road trip to northern Iran to market 130kg of pistachios. Sleeping in their car and selling door-to-door, they proved that perseverance is an entrepreneur’s greatest asset.": {
        "en": "Joined by Hassan Dolatabadi, the team embarked on a challenging road trip to northern Iran to market 130kg of pistachios. Sleeping in their car and selling door-to-door, they proved that perseverance is an entrepreneur’s greatest asset.",
        "fa": "با پیوستن حسن دولت‌آبادی، تیم سفری پرچالش را با ۱۳۰ کیلوگرم پسته به شمال ایران آغاز کرد. آن‌ها با استراحت در خودرو و فروش خانه‌به‌خانه، ثابت کردند که پشتکار بزرگترین سرمایه یک کارآفرین است.",
        "ar": "بانضمام حسن دولت آبادي، انطلق الفريق في رحلة شاقة إلى شمال إيران لتسويق ۱۳۰ كيلوغراماً من الفستق. من خلال النوم في سيارتهم والبيع من باب إلى باب، أثبتوا أن المثابرة هي أعظم أصول رائد الأعمال.",
        "tr": "Hassan Dolatabadi'nin katılımıyla ekip, 130 kg fıstığı pazarlamak için kuzey İran'a zorlu bir yolculuğa çıktı. Arabalarında uyuyup kapı kapı satış yaparak, azmin bir girişimcinin en büyük varlığı olduğunu kanıtladılar."
    },
    "Expansion": {
        "en": "Expansion",
        "fa": "توسعه",
        "ar": "التوسع",
        "tr": "Büyüme"
    },
    "Industrial Growth": {
        "en": "Industrial Growth",
        "fa": "رشد صنعتی",
        "ar": "النمو الصناعي",
        "tr": "Endüstriyel Büyüme"
    },
    "Growing trust from customers led to the opening of the central office and a larger urban workshop. The integration of modern sorting and processing machinery elevated production capacity and quality to a new level.": {
        "en": "Growing trust from customers led to the opening of the central office and a larger urban workshop. The integration of modern sorting and processing machinery elevated production capacity and quality to a new level.",
        "fa": "اعتماد روزافزون مشتریان منجر به تأسیس دفتر مرکزی و یک کارگاه بزرگتر شهری شد. بهره‌گیری از دستگاه‌های مدرن سورتینگ و فرآوری، ظرفیت تولید و کیفیت را به سطح جدیدی ارتقا داد.",
        "ar": "أدت الثقة المتزايدة من العملاء إلى افتتاح المكتب المركزي وورشة عمل حضرية أكبر. رفع دمج آلات الفرز والمعالجة الحديثة الطاقة الإنتاجية والجودة إلى مستوى جديد.",
        "tr": "Müşterilerden gelen artan güven, merkez ofisin ve daha büyük bir şehir atölyesinin açılmasına yol açtı. Modern ayıklama ve işleme makinelerinin entegrasyonu, üretim kapasitesini ve kaliteyi yeni bir seviyeye taşıdı."
    },
    "Present": {
        "en": "Present",
        "fa": "امروز",
        "ar": "اليوم",
        "tr": "Bugün"
    },
    "Global Recognition": {
        "en": "Global Recognition",
        "fa": "اعتبار جهانی",
        "ar": "اعتراف عالمي",
        "tr": "Küresel Tanınma"
    },
    "Today, Palace Karimi operates with 25 dedicated experts, exporting to the UAE, Turkey, and the UK. Hossein Karimi proudly serves as the youngest member of the Iran Chamber of Commerce, driving international trade forward.": {
        "en": "Today, Palace Karimi operates with 25 dedicated experts, exporting to the UAE, Turkey, and the UK. Hossein Karimi proudly serves as the youngest member of the Iran Chamber of Commerce, driving international trade forward.",
        "fa": "امروز، بازرگانی پالِس کریمی با ۲۵ نیروی متخصص فعالیت می‌کند و محصولات خود را به امارات، ترکیه و انگلستان صادر می‌نماید. حسین کریمی نیز به‌عنوان کوچکترین عضو اتاق بازرگانی ایران، مسیر توسعه تجارت بین‌المللی را پیش می‌برد.",
        "ar": "اليوم، تعمل بالس كريمي مع ۲۵ خبيراً متخصصاً، وتصدر إلى الإمارات العربية المتحدة وتركيا والمملكة المتحدة. يخدم حسين كريمي بفخر كأصغر عضو في غرفة التجارة الإيرانية، دافعاً التجارة الدولية إلى الأمام.",
        "tr": "Bugün Palace Karimi, BAE, Türkiye ve Birleşik Krallık'a ihracat yapan 25 uzmanla çalışmaktadır. Hossein Karimi, İran Ticaret Odası'nın en genç üyesi olarak gururla hizmet vermekte ve uluslararası ticareti ileriye taşımaktadır."
    },
    "About": {
        "en": "About",
        "fa": "درباره",
        "ar": "حول",
        "tr": "Hakkında"
    },

    "Palace Karimi": {
        "en": "Palace Karimi",
        "fa": "پالِس کریمی",
        "ar": "بالس كريمي",
        "tr": "Palace Karimi"
    },

    "Hossein Karimi Trading, operating under the Palace Karimi brand and managed by Mr. Hossein Karimi, is a dynamic and growing enterprise. With a dedicated team of 25 experts, we specialize in supplying, packaging, and exporting premium Iranian saffron and pistachios.": {
        "en": "Hossein Karimi Trading, operating under the Palace Karimi brand and managed by Mr. Hossein Karimi, is a dynamic and growing enterprise. With a dedicated team of 25 experts, we specialize in supplying, packaging, and exporting premium Iranian saffron and pistachios.",
        "fa": "بازرگانی حسین کریمی با برند (پالس کریمی) به مدیریت آقای حسین کریمی، امروزه با بهره‌گیری از تیمی متشکل از ۲۵ نیروی متخصص و متعهد، مجموعه‌ای پویا و رو به رشد در حوزه تأمین، بسته‌بندی و صادرات پسته و زعفران ممتاز ایران فعالیت می‌کند.",
        "ar": "تعمل شركة حسين كريمي التجارية، تحت علامة بالس كريمي التجارية وبإدارة السيد حسين كريمي، كمؤسسة ديناميكية ومتنامية. بفضل فريق متخصص مكون من ۲۵ خبيراً، ننشط في توريد وتعبئة وتصدير الزعفران والفستق الإيراني الممتاز.",
        "tr": "Palace Karimi markası altında ve Sayın Hossein Karimi yönetiminde faaliyet gösteren Hossein Karimi Ticaret, dinamik ve büyüyen bir kuruluştur. 25 kişilik uzman ekibimizle birinci sınıf İran safranı ve fıstığı tedarik, paketleme ve ihracatında faaliyet gösteriyoruz."
    },

    "By combining experience, market knowledge, and a commitment to quality, we strive to build a reliable bridge between Iranian producers and global markets. Every stage of our operation, from meticulous product selection to packaging and shipping, is conducted under strict professional standards and continuous supervision to ensure our customers always receive premium and reliable products.": {
        "en": "By combining experience, market knowledge, and a commitment to quality, we strive to build a reliable bridge between Iranian producers and global markets. Every stage of our operation, from meticulous product selection to packaging and shipping, is conducted under strict professional standards and continuous supervision to ensure our customers always receive premium and reliable products.",
        "fa": "ما با تلفیق تجربه، دانش بازار و تعهد به کیفیت، تلاش کرده‌ایم پلی مطمئن میان تولیدکنندگان ایرانی و بازارهای جهان ایجاد کنیم. تمامی مراحل فعالیت مجموعه، از انتخاب دقیق محصولات تا بسته‌بندی و ارسال، با رعایت استانداردهای حرفه‌ای و نظارت مستمر انجام می‌شود تا مشتریان ما همواره محصولی ممتاز و قابل اعتماد دریافت کنند.",
        "ar": "من خلال الجمع بين الخبرة ومعرفة السوق والالتزام بالجودة، سعينا لبناء جسر موثوق بين المنتجين الإيرانيين والأسواق العالمية. تتم جميع مراحل عملنا، من الاختيار الدقيق للمنتجات إلى التعبئة والشحن، وفقاً للمعايير المهنية والإشراف المستمر لضمان حصول عملائنا دائماً على منتجات ممتازة وموثوقة.",
        "tr": "Deneyim, pazar bilgisi ve kalite taahhüdünü birleştirerek, İranlı üreticiler ile küresel pazarlar arasında güvenilir bir köprü kurmaya çalışıyoruz. Müşterilerimizin her zaman birinci sınıf ve güvenilir ürünler almasını sağlamak için, dikkatli ürün seçiminden paketleme ve sevkiyata kadar her aşama sıkı profesyonel standartlar ve sürekli denetim altında gerçekleştirilir."
    },

    "At Palace Karimi, quality is not just a standard; it is a commitment that flows through all our partnerships and services. Our vision is to become an enduring and trusted name in the global trade of authentic Persian products, forging long-term collaborations with business partners worldwide.": {
        "en": "At Palace Karimi, quality is not just a standard; it is a commitment that flows through all our partnerships and services. Our vision is to become an enduring and trusted name in the global trade of authentic Persian products, forging long-term collaborations with business partners worldwide.",
        "fa": "در پالس کریمی، کیفیت تنها یک استاندارد نیست، بلکه تعهدی است که در تمامی همکاری‌ها و خدمات ما جریان دارد. چشم‌انداز ما، تبدیل شدن به یکی از نام‌های ماندگار و قابل اعتماد در تجارت جهانی محصولات اصیل ایرانی و ایجاد همکاری‌های بلندمدت با شرکای تجاری در سراسر جهان است.",
        "ar": "في بالس كريمي، الجودة ليست مجرد معيار، بل هي التزام يتدفق عبر جميع شراكاتنا وخدماتنا. رؤيتنا هي أن نصبح اسماً خالداً وموثوقاً في التجارة العالمية للمنتجات الإيرانية الأصيلة، وإقامة تعاون طويل الأمد مع شركاء تجاريين في جميع أنحاء العالم.",
        "tr": "Palace Karimi'de kalite sadece bir standart değil; tüm işbirliklerimiz ve hizmetlerimiz boyunca akan bir taahhüttür. Vizyonumuz, dünya çapındaki iş ortaklarıyla uzun vadeli işbirlikleri kurarak otantik İran ürünlerinin küresel ticaretinde kalıcı ve güvenilir bir isim olmaktır."
    },
    "God provides sustenance without measure.": {
        "en": "God provides sustenance without measure.",
        "fa": "خدا روزی‌رسان بی‌حساب است.",
        "ar": "الله هو الرزاق بغير حساب.",
        "tr": "Allah hesapsız rızık verendir."
    },
}


def update_translations():
    for lang, _ in [('fa', 'Persian'), ('ar', 'Arabic'), ('tr', 'Turkish')]:
        po_path = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.po')

        if not os.path.exists(po_path):
            print(f"File not found: {po_path}. Skipping {lang}.")
            continue

        po = polib.pofile(po_path)

        for msgid, trans_dict in TRANSLATIONS.items():
            if lang in trans_dict:
                entry = po.find(msgid)
                if entry:
                    entry.msgstr = trans_dict[lang]
                else:
                    entry = polib.POEntry(
                        msgid=msgid,
                        msgstr=trans_dict[lang]
                    )
                    po.append(entry)

        po.save(po_path)
        print(f"Updated {po_path}")


if __name__ == '__main__':
    print("Starting translation update...")
    update_translations()
    print("Done. Now run: python manage.py compilemessages")