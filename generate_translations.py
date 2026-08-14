import os
import polib

LOCALE_DIR = 'locale'
LANGS = ['en', 'fa', 'ar', 'tr']

# ---------------------------------------------------------------------------
# دیکشنری جامع ترجمه‌ها برای ۳ زبان (فارسی، عربی، ترکی)
# انگلیسی به‌صورت خودکار از کلید msgid استفاده می‌کند.
# ---------------------------------------------------------------------------
TRANSLATIONS = {
    # ------------------------------------------------------------------
    # پیام‌ها و اعلان‌های سیستم
    # ------------------------------------------------------------------
    "You have sent too many messages. Please try again later.": {
        "fa": "تعداد پیام‌های شما بیش از حد مجاز است. لطفاً بعداً دوباره تلاش کنید.",
        "ar": "لقد أرسلت عددًا كبيرًا جدًا من الرسائل. يرجى المحاولة مرة أخرى لاحقًا.",
        "tr": "Çok fazla mesaj gönderdiniz. Lütfen daha sonra tekrar deneyiniz."
    },
    "Your message has been sent successfully. We will contact you soon.": {
        "fa": "پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.",
        "ar": "تم إرسال رسالتك بنجاح. سنتواصل معك قريبًا.",
        "tr": "Mesajınız başarıyla gönderildi. En kısa sürede sizinle iletişime geçeceğiz."
    },
    "success_contact": {
        "fa": "پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.",
        "ar": "تم إرسال رسالتك بنجاح. سنتواصل معك قريبًا.",
        "tr": "Mesajınız başarıyla gönderildi. En kısa sürede sizinle iletişime geçeceğiz."
    },
    "Too many requests. Please try again later.": {
        "fa": "تعداد درخواست‌ها بیش از حد مجاز است. لطفاً بعداً دوباره تلاش کنید.",
        "ar": "طلبات كثيرة جدًا. يرجى المحاولة مرة أخرى لاحقًا.",
        "tr": "Çok fazla istek. Lütfen daha sonra tekrar deneyiniz."
    },
    "Please enter an email address.": {
        "fa": "لطفاً یک آدرس ایمیل وارد کنید.",
        "ar": "يرجى إدخال البريد الإلكتروني.",
        "tr": "Lütfen bir e-posta adresi girin."
    },
    "Thank you for subscribing to our newsletter.": {
        "fa": "با تشکر از عضویت شما در خبرنامه.",
        "ar": "شكرًا لاشتراكك في نشرتنا الإخبارية.",
        "tr": "Bültenimize abone olduğunuz için teşekkür ederiz."
    },
    "You are already subscribed to our email list.": {
        "fa": "شما قبلاً در خبرنامه ثبت‌نام کرده‌اید.",
        "ar": "أنت مشترك بالفعل في قائمتنا البريدية.",
        "tr": "E-posta listemize zaten abonesiniz."
    },
    "Invalid email address. Please check and try again.": {
        "fa": "آدرس ایمیل نامعتبر است. لطفاً بررسی و دوباره تلاش کنید.",
        "ar": "عنوان البريد الإلكتروني غير صالح. يرجى التحقق والمحاولة مرة أخرى.",
        "tr": "Geçersiz e-posta adresi. Lütfen kontrol edip tekrar deneyin."
    },

    # ------------------------------------------------------------------
    # اعتبارسنجی فرم‌ها
    # ------------------------------------------------------------------
    "Your message is too short. Please provide more details (minimum 20 characters).": {
        "fa": "متن پیام شما بسیار کوتاه است. لطفاً اطلاعات بیشتری وارد کنید (حداقل ۲۰ کاراکتر).",
        "ar": "رسالتك قصيرة جدًا. يرجى تقديم المزيد من التفاصيل (۲۰ حرفًا على الأقل).",
        "tr": "Mesajınız çok kısa. Lütfen daha fazla detay verin (en az 20 karakter)."
    },
    "Spam bot detected!": {
        "fa": "ربات اسپم شناسایی شد!",
        "ar": "تم اكتشاف برنامج روبوت للبريد العشوائي!",
        "tr": "Spam botu tespit edildi!"
    },
    "Phone Extension": {
        "fa": "پیش‌شماره تلفن",
        "ar": "تحويلة الهاتف",
        "tr": "Dahili Telefon"
    },

    # ------------------------------------------------------------------
    # هدر، فوتر و ناوبری
    # ------------------------------------------------------------------
    "Home": {
        "fa": "خانه",
        "ar": "الرئيسية",
        "tr": "Ana Sayfa"
    },
    "About Us": {
        "fa": "درباره ما",
        "ar": "من نحن",
        "tr": "Hakkımızda"
    },
    "Products": {
        "fa": "محصولات",
        "ar": "المنتجات",
        "tr": "Ürünler"
    },
    "Contact Us": {
        "fa": "تماس با ما",
        "ar": "اتصل بنا",
        "tr": "İletişim"
    },
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
        "fa": "برای دریافت آخرین به‌روزرسانی‌ها و پیشنهادهای ویژه در خبرنامه ما عضو شوید.",
        "ar": "اشترك في نشرتنا الإخبارية للحصول على آخر التحديثات والعروض الفاخرة.",
        "tr": "En güncel haberler ve lüks tekliflerden haberdar olmak için bültenimize abone olun."
    },
    "Success!": {
        "fa": "موفقیت!",
        "ar": "نجاح!",
        "tr": "Başarılı!"
    },
    "You have been added to our email list.": {
        "fa": "شما به لیست ایمیل ما اضافه شدید.",
        "ar": "تمت إضافتك إلى قائمتنا البريدية.",
        "tr": "E-posta listemize eklendiniz."
    },
    "Email Address": {
        "fa": "آدرس ایمیل",
        "ar": "البريد الإلكتروني",
        "tr": "E-posta Adresi"
    },
    "Subscribe": {
        "fa": "عضویت",
        "ar": "اشترك",
        "tr": "Abone Ol"
    },
    "Latest Tweets": {
        "fa": "آخرین توییت‌ها",
        "ar": "أحدث التغريدات",
        "tr": "Son Tweetler"
    },
    "Please wait...": {
        "fa": "لطفاً صبر کنید...",
        "ar": "يرجى الانتظار...",
        "tr": "Lütfen bekleyin..."
    },
    "Tehran, Iran": {
        "fa": "تهران، ایران",
        "ar": "طهران، إيران",
        "tr": "Tahran, İran"
    },
    "Follow Us": {
        "fa": "ما را دنبال کنید",
        "ar": "تابعنا",
        "tr": "Bizi Takip Edin"
    },
    "© 2026 Palace Karimi. All Rights Reserved.": {
        "fa": "© ۲۰۲۶ پالاس کریمی. تمامی حقوق محفوظ است.",
        "ar": "© ۲۰۲۶ قصر كريمي. جميع الحقوق محفوظة.",
        "tr": "© 2026 Palace Karimi. Tüm hakları saklıdır."
    },
    "Designed & Developed by": {
        "fa": "طراحی و توسعه توسط",
        "ar": "تصميم وتطوير بواسطة",
        "tr": "Tasarım ve Geliştirme"
    },
    "FAQ": {
        "fa": "سوالات متداول",
        "ar": "الأسئلة الشائعة",
        "tr": "SSS"
    },
    "Sitemap": {
        "fa": "نقشه سایت",
        "ar": "خريطة الموقع",
        "tr": "Site Haritası"
    },
    "Notifications": {
        "fa": "اعلان‌ها",
        "ar": "الإشعارات",
        "tr": "Bildirimler"
    },

    # ------------------------------------------------------------------
    # کاتالوگ و فروشگاه
    # ------------------------------------------------------------------
    "Sale!": {
        "fa": "حراج!",
        "ar": "تخفيض!",
        "tr": "İndirim!"
    },
    "Contact for Price": {
        "fa": "تماس برای قیمت",
        "ar": "اتصل لمعرفة السعر",
        "tr": "Fiyat için İletişim"
    },
    "Price not set": {
        "fa": "قیمت تعیین نشده",
        "ar": "السعر غير محدد",
        "tr": "Fiyat Belirlenmedi"
    },
    "No products available in this category.": {
        "fa": "هیچ محصولی در این دسته‌بندی موجود نیست.",
        "ar": "لا توجد منتجات في هذا القسم.",
        "tr": "Bu kategoride ürün bulunmamaktadır."
    },
    "Description": {
        "fa": "توضیحات",
        "ar": "الوصف",
        "tr": "Açıklama"
    },
    "Additional Info": {
        "fa": "اطلاعات بیشتر",
        "ar": "معلومات إضافية",
        "tr": "Ek Bilgi"
    },
    "Related Products": {
        "fa": "محصولات مرتبط",
        "ar": "منتجات ذات صلة",
        "tr": "İlgili Ürünler"
    },
    "Category": {
        "fa": "دسته‌بندی",
        "ar": "الفئة",
        "tr": "Kategori"
    },

    # ------------------------------------------------------------------
    # برند و عناوین عمومی
    # ------------------------------------------------------------------
    "Palace Karimi": {
        "fa": "پالاس کریمی",
        "ar": "قصر كريمي",
        "tr": "Palace Karimi"
    },
    "404 - Page Not Found": {
        "fa": "۴۰۴ - صفحه مورد نظر پیدا نشد",
        "ar": "۴۰۴ - الصفحة غير موجودة",
        "tr": "404 - Sayfa Bulunamadı"
    },
    "500 - Internal Server Error": {
        "fa": "۵۰۰ - خطای داخلی سرور",
        "ar": "۵۰۰ - خطأ في الخادم الداخلي",
        "tr": "500 - Sunucu Hatası"
    },
    "Back to Home": {
        "fa": "بازگشت به صفحه اصلی",
        "ar": "العودة إلى الرئيسية",
        "tr": "Ana Sayfaya Dön"
    },

    # ------------------------------------------------------------------
    # بخش اصلی صفحه نخست
    # ------------------------------------------------------------------
    "The Finest Quality": {
        "fa": "بالاترین کیفیت",
        "ar": "أعلى جودة",
        "tr": "En Yüksek Kalite"
    },
    "PREMIUM SAFFRON": {
        "fa": "زعفران ممتاز",
        "ar": "زعفران فاخر",
        "tr": "PREMIUM SAFRAN"
    },
    "Experience the true taste of luxury.": {
        "fa": "طعم واقعی لوکس بودن را تجربه کنید.",
        "ar": "جرّب المذاق الحقيقي للفخامة.",
        "tr": "Lüksün gerçek tadını yaşayın."
    },
    "Exporting Worldwide": {
        "fa": "صادرات به سراسر جهان",
        "ar": "تصدير إلى جميع أنحاء العالم",
        "tr": "Dünya Geneline İhracat"
    },
    "PERSIAN PISTACHIO": {
        "fa": "پسته ایرانی",
        "ar": "فستق فارسي",
        "tr": "PERSIAN FISTIK"
    },
    "Hand-picked and premium quality.": {
        "fa": "چیده شده با دست و با کیفیت عالی.",
        "ar": "مختارة يدويًا وبجودة ممتازة.",
        "tr": "Elle toplanmış ve birinci sınıf kalite."
    },
    "YOUR TRUSTED PARTNER": {
        "fa": "شریک مورد اعتماد شما",
        "ar": "شريكك الموثوق",
        "tr": "GÜVENİLİR ORTAĞINIZ"
    },
    "Providing the best agricultural products.": {
        "fa": "ارائه بهترین محصولات کشاورزی.",
        "ar": "توفير أفضل المنتجات الزراعية.",
        "tr": "En iyi tarım ürünlerini sağlıyoruz."
    },
    "Follow us on social media for the latest updates and news!": {
        "fa": "برای آخرین اخبار و به‌روزرسانی‌ها ما را در شبکه‌های اجتماعی دنبال کنید!",
        "ar": "تابعنا على وسائل التواصل الاجتماعي لآخر التحديثات والأخبار!",
        "tr": "En son güncellemeler ve haberler için bizi sosyal medyada takip edin!"
    },
    "Experience a secure purchase with the top exporter of authentic Iranian products": {
        "fa": "با برترین صادرکننده محصولات اصیل ایرانی، خریدی مطمئن را تجربه کنید",
        "ar": "استمتع بعملية شراء آمنة مع أفضل مصدّر للمنتجات الإيرانية الأصيلة",
        "tr": "Orijinal İran ürünlerinin en iyi ihracatçısıyla güvenli bir alışveriş deneyimi yaşayın"
    },
    "Demand the best quality saffron and pistachio from us.": {
        "fa": "بهترین کیفیت زعفران و پسته را از ما بخواهید.",
        "ar": "اطلب أجود أنواع الزعفران والفستق منا.",
        "tr": "En kaliteli safran ve fıstığı bizden isteyin."
    },
    "Contact Experts": {
        "fa": "تماس با کارشناسان",
        "ar": "تواصل مع الخبراء",
        "tr": "Uzmanlarla İletişime Geçin"
    },
    "or": {
        "fa": "یا",
        "ar": "أو",
        "tr": "veya"
    },
    "view products.": {
        "fa": "مشاهده محصولات.",
        "ar": "عرض المنتجات.",
        "tr": "ürünleri görüntüleyin."
    },
    "Palace Karimi is a brand that is": {
        "fa": "پالاس کریمی برندی است که",
        "ar": "قصر كريمي علامة تجارية تتميز بأنها",
        "tr": "Palace Karimi öyle bir markadır ki"
    },
    "Authentic": {
        "fa": "اصیل",
        "ar": "أصيلة",
        "tr": "Otantik"
    },
    "High Quality": {
        "fa": "کیفیت بالا",
        "ar": "جودة عالية",
        "tr": "Yüksek Kalite"
    },
    "Global": {
        "fa": "جهانی",
        "ar": "عالمية",
        "tr": "Küresel"
    },
    "and a secure choice for export.": {
        "fa": "و انتخابی مطمئن برای صادرات.",
        "ar": "وخيار آمن للتصدير.",
        "tr": "ve ihracat için güvenli bir seçimdir."
    },
    "Experience the pinnacle of luxury with Palace Karimi": {
        "fa": "اوج تجمل را با پالاس کریمی تجربه کنید",
        "ar": "استمتع بقمة الفخامة مع قصر كريمي",
        "tr": "Palace Karimi ile lüksün zirvesini yaşayın"
    },
    "Consultation": {
        "fa": "مشاوره",
        "ar": "استشارة",
        "tr": "Danışmanlık"
    },
    "Harvesting": {
        "fa": "برداشت",
        "ar": "الحصاد",
        "tr": "Hasat"
    },
    "Processing": {
        "fa": "فرآوری",
        "ar": "المعالجة",
        "tr": "İşleme"
    },
    "Packaging": {
        "fa": "بسته‌بندی",
        "ar": "التعبئة والتغليف",
        "tr": "Paketleme"
    },
    "Global Export": {
        "fa": "صادرات جهانی",
        "ar": "التصدير العالمي",
        "tr": "Küresel İhracat"
    },
    "New": {
        "fa": "جدید",
        "ar": "جديد",
        "tr": "Yeni"
    },
    "View Details": {
        "fa": "مشاهده جزئیات",
        "ar": "عرض التفاصيل",
        "tr": "Detayları Gör"
    },
    "No products available.": {
        "fa": "هیچ محصولی موجود نیست.",
        "ar": "لا توجد منتجات متاحة.",
        "tr": "Mevcut ürün yok."
    },
    "Why Choose": {
        "fa": "چرا انتخاب کنید",
        "ar": "لماذا تختار",
        "tr": "Neden Seçmelisiniz"
    },
    "Palace Karimi?": {
        "fa": "پالاس کریمی؟",
        "ar": "قصر كريمي؟",
        "tr": "Palace Karimi?"
    },
    "Pure, natural products cultivated without harmful chemicals.": {
        "fa": "محصولات خالص و طبیعی که بدون مواد شیمیایی مضر کشت شده‌اند.",
        "ar": "منتجات نقية وطبيعية مزروعة بدون مواد كيميائية ضارة.",
        "tr": "Zararlı kimyasallar olmadan yetiştirilen saf ve doğal ürünler."
    },
    "Premium Quality": {
        "fa": "کیفیت برتر",
        "ar": "جودة ممتازة",
        "tr": "Birinci Sınıf Kalite"
    },
    "Export-grade saffron and pistachio carefully hand-picked.": {
        "fa": "زعفران و پسته با کیفیت صادراتی که با دقت دست‌چین شده‌اند.",
        "ar": "زعفران وفستق بجودة التصدير، مختارة يدويًا بعناية.",
        "tr": "İhracat kalitesinde, özenle elle toplanmış safran ve fıstık."
    },
    "Luxury Packaging": {
        "fa": "بسته‌بندی لوکس",
        "ar": "تغليف فاخر",
        "tr": "Lüks Paketleme"
    },
    "Elegant and secure packaging maintaining freshness and aroma.": {
        "fa": "بسته‌بندی شیک و ایمن که تازگی و عطر را حفظ می‌کند.",
        "ar": "تغليف أنيق وآمن يحافظ على النضارة والرائحة.",
        "tr": "Tazelik ve aromayı koruyan zarif ve güvenli paketleme."
    },
    "Lab Certified": {
        "fa": "دارای گواهی آزمایشگاهی",
        "ar": "معتمد مختبريًا",
        "tr": "Laboratuvar Sertifikalı"
    },
    "Rigorous laboratory testing for color, flavor, and purity.": {
        "fa": "آزمایش‌های دقیق آزمایشگاهی برای رنگ، طعم و خلوص.",
        "ar": "اختبارات مخبرية صارمة للون والنكهة والنقاء.",
        "tr": "Renk, tat ve saflık için titiz laboratuvar testleri."
    },
    "Direct from Farms": {
        "fa": "مستقیم از مزارع",
        "ar": "مباشرة من المزارع",
        "tr": "Doğrudan Çiftliklerden"
    },
    "Sourced directly from the best Iranian agricultural lands.": {
        "fa": "مستقیماً از بهترین زمین‌های کشاورزی ایران تهیه شده است.",
        "ar": "مصدرها مباشرة من أفضل الأراضي الزراعية الإيرانية.",
        "tr": "Doğrudan en iyi İran tarım arazilerinden temin edilmektedir."
    },
    "Wholesale Supply": {
        "fa": "تأمین عمده",
        "ar": "توريد بالجملة",
        "tr": "Toptan Tedarik"
    },
    "Capability to fulfill bulk orders for businesses worldwide.": {
        "fa": "توانایی تأمین سفارش‌های عمده برای کسب‌وکارها در سراسر جهان.",
        "ar": "القدرة على تلبية الطلبات بالجملة للشركات في جميع أنحاء العالم.",
        "tr": "Dünya çapındaki işletmeler için toplu siparişleri karşılama kapasitesi."
    },
    "24/7 Support": {
        "fa": "پشتیبانی ۲۴/۷",
        "ar": "دعم على مدار الساعة",
        "tr": "7/24 Destek"
    },
    "Dedicated customer service and consultation for our partners.": {
        "fa": "خدمات مشتریان و مشاوره اختصاصی برای شرکای ما.",
        "ar": "خدمة عملاء واستشارات مخصصة لشركائنا.",
        "tr": "Ortaklarımız için özel müşteri hizmetleri ve danışmanlık."
    },
    "Our Guarantees": {
        "fa": "تضمین‌های ما",
        "ar": "ضماناتنا",
        "tr": "Garantilerimiz"
    },
    "Authenticity Guarantee": {
        "fa": "تضمین اصالت",
        "ar": "ضمان الأصالة",
        "tr": "Orijinallik Garantisi"
    },
    "International Standards": {
        "fa": "استانداردهای بین‌المللی",
        "ar": "المعايير الدولية",
        "tr": "Uluslararası Standartlar"
    },
    "Our products are processed and packaged strictly according to international food safety and hygiene standards.": {
        "fa": "محصولات ما دقیقاً مطابق با استانداردهای بین‌المللی ایمنی و بهداشت مواد غذایی فرآوری و بسته‌بندی می‌شوند.",
        "ar": "تتم معالجة منتجاتنا وتغليفها بدقة وفقًا لمعايير سلامة الأغذية والنظافة الدولية.",
        "tr": "Ürünlerimiz uluslararası gıda güvenliği ve hijyen standartlarına tam uygun olarak işlenir ve paketlenir."
    },
    "Custom White-Labeling": {
        "fa": "برچسب سفارشی",
        "ar": "العلامة التجارية الخاصة",
        "tr": "Özel Etiketleme"
    },
    "We offer exclusive custom packaging and white-labeling services for your brand to stand out in the global market.": {
        "fa": "ما خدمات بسته‌بندی سفارشی و برچسب اختصاصی ارائه می‌دهیم تا برند شما در بازار جهانی متمایز شود.",
        "ar": "نقدم خدمات التغليف المخصص والعلامة التجارية الخاصة لعلامتك التجارية لتتميز في السوق العالمية.",
        "tr": "Markanızın küresel pazarda öne çıkması için özel paketleme ve etiketleme hizmetleri sunuyoruz."
    },
    "We proudly export our products to": {
        "fa": "ما با افتخار محصولات خود را به",
        "ar": "نحن بفخر نصدر منتجاتنا إلى",
        "tr": "Ürünlerimizi gururla şu bölgelere ihraç ediyoruz"
    },
    "Europe": {
        "fa": "اروپا",
        "ar": "أوروبا",
        "tr": "Avrupa"
    },
    "Asia": {
        "fa": "آسیا",
        "ar": "آسيا",
        "tr": "Asya"
    },
    "Middle East": {
        "fa": "خاورمیانه",
        "ar": "الشرق الأوسط",
        "tr": "Orta Doğu"
    },
    "Trusted by leading international businesses and distributors worldwide.": {
        "fa": "مورد اعتماد کسب‌وکارها و توزیع‌کنندگان پیشرو بین‌المللی در سراسر جهان.",
        "ar": "موثوق به من قبل الشركات والموزعين الدوليين الرائدين في جميع أنحاء العالم.",
        "tr": "Dünya çapındaki önde gelen uluslararası işletmeler ve distribütörler tarafından güvenilmektedir."
    },
    "Introduce": {
        "fa": "معرفی",
        "ar": "تقديم",
        "tr": "Tanıtım"
    },
    "Us": {
        "fa": "ما",
        "ar": "نحن",
        "tr": "Biz"
    },
    "Palace Karimi is a leading exporter of premium agricultural products. Sourced directly from the finest farms, our saffron and pistachios undergo rigorous quality control.": {
        "fa": "پالاس کریمی صادرکننده پیشرو محصولات کشاورزی ممتاز است. زعفران و پسته ما مستقیماً از بهترین مزارع تهیه شده و تحت کنترل کیفی دقیق قرار می‌گیرند.",
        "ar": "قصر كريمي هو مصدّر رائد للمنتجات الزراعية الفاخرة. زعفراننا وفستقنا يتم الحصول عليهما مباشرة من أفضل المزارع ويخضعان لرقابة جودة صارمة.",
        "tr": "Palace Karimi, birinci sınıf tarım ürünlerinin lider ihracatçısıdır. En iyi çiftliklerden doğrudan temin edilen safran ve fıstıklarımız titiz kalite kontrolden geçer."
    },
    "Read More": {
        "fa": "بیشتر بخوانید",
        "ar": "اقرأ المزيد",
        "tr": "Daha Fazla Oku"
    },
    "Our commitment to excellence ensures that every product reaching your hands meets the highest international standards.": {
        "fa": "تعهد ما به برتری تضمین می‌کند هر محصولی که به دست شما می‌رسد بالاترین استانداردهای بین‌المللی را رعایت کند.",
        "ar": "إن التزامنا بالتميز يضمن أن كل منتج يصل إلى يديك يفي بأعلى المعايير الدولية.",
        "tr": "Mükemmelliğe olan bağlılığımız, elinize ulaşan her ürünün en yüksek uluslararası standartları karşılamasını sağlar."
    },
    "We utilize state-of-the-art sorting and packaging technologies to preserve the natural aroma, flavor, and nutritional value of our products.": {
        "fa": "ما از فناوری‌های پیشرفته تفکیک و بسته‌بندی برای حفظ عطر، طعم و ارزش غذایی طبیعی محصولات خود استفاده می‌کنیم.",
        "ar": "نستخدم أحدث تقنيات الفرز والتغليف للحفاظ على الرائحة والنكهة والقيمة الغذائية الطبيعية لمنتجاتنا.",
        "tr": "Ürünlerimizin doğal aromasını, tadını ve besin değerini korumak için en son teknoloji ayıklama ve paketleme teknolojilerini kullanıyoruz."
    },
    "Our Vision": {
        "fa": "چشم‌انداز ما",
        "ar": "رؤيتنا",
        "tr": "Vizyonumuz"
    },
    "To be the most trusted and recognized global brand for luxury Persian saffron and premium pistachios, setting the benchmark for quality, purity, and sustainable agriculture in the international market.": {
        "fa": "تبدیل شدن به معتبرترین و شناخته‌شده‌ترین برند جهانی زعفران لوکس ایرانی و پسته ممتاز، و تعیین معیار کیفیت، خلوص و کشاورزی پایدار در بازار بین‌المللی.",
        "ar": "أن نكون العلامة التجارية العالمية الأكثر ثقة واعترافًا للزعفران الفارسي الفاخر والفستق الممتاز، واضعين المعيار للجودة والنقاء والزراعة المستدامة في السوق الدولية.",
        "tr": "Uluslararası pazarda kalite, saflık ve sürdürülebilir tarım için ölçüt belirleyen, lüks İran safranı ve birinci sınıf fıstık için en güvenilir ve tanınan küresel marka olmak."
    },
    "Our Mission": {
        "fa": "ماموریت ما",
        "ar": "مهمتنا",
        "tr": "Misyonumuz"
    },
    "Licenses & Certificates": {
        "fa": "مجوزها و گواهینامه‌ها",
        "ar": "التراخيص والشهادات",
        "tr": "Lisanslar ve Sertifikalar"
    },
    "Quality Management System": {
        "fa": "سیستم مدیریت کیفیت",
        "ar": "نظام إدارة الجودة",
        "tr": "Kalite Yönetim Sistemi"
    },
    "Organic Certified": {
        "fa": "دارای گواهی ارگانیک",
        "ar": "معتمد عضويًا",
        "tr": "Organik Sertifikalı"
    },
    "Phytosanitary": {
        "fa": "بهداشت گیاهی",
        "ar": "الصحة النباتية",
        "tr": "Bitki Sağlığı"
    },
    "Global Health & Safety": {
        "fa": "سلامت و ایمنی جهانی",
        "ar": "الصحة والسلامة العالمية",
        "tr": "Küresel Sağlık ve Güvenlik"
    },
    "Export Standard Approval": {
        "fa": "تأیید استاندارد صادراتی",
        "ar": "اعتماد معيار التصدير",
        "tr": "İhracat Standardı Onayı"
    },
    "Our": {
        "fa": "ما",
        "ar": "خاصتنا",
        "tr": "Bizim"
    },
    "History": {
        "fa": "تاریخچه",
        "ar": "التاريخ",
        "tr": "Tarihçe"
    },
    "From a passionate family-owned farm to a recognized global export enterprise.": {
        "fa": "از یک مزرعه خانوادگی پرشور تا یک شرکت صادراتی جهانی شناخته‌شده.",
        "ar": "من مزرعة عائلية شغوفة إلى مؤسسة تصدير عالمية معترف بها.",
        "tr": "Tutkulu bir aile çiftliğinden tanınmış bir küresel ihracat kuruluşuna."
    },
    "Global Expansion": {
        "fa": "توسعه جهانی",
        "ar": "التوسع العالمي",
        "tr": "Küresel Genişleme"
    },
    "Palace Karimi officially expanded its export lines to Europe and the Middle East, acquiring major international licenses.": {
        "fa": "پالاس کریمی رسماً خطوط صادراتی خود را به اروپا و خاورمیانه گسترش داد و مجوزهای بین‌المللی عمده‌ای دریافت کرد.",
        "ar": "وسّعت قصر كريمي رسميًا خطوط التصدير إلى أوروبا والشرق الأوسط، وحصلت على تراخيص دولية كبرى.",
        "tr": "Palace Karimi, ihracat hatlarını resmî olarak Avrupa ve Orta Doğu'ya genişletti ve önemli uluslararası lisanslar aldı."
    },
    "Modern Facilities": {
        "fa": "تجهیزات مدرن",
        "ar": "مرافق حديثة",
        "tr": "Modern Tesisler"
    },
    "The Beginning": {
        "fa": "آغاز",
        "ar": "البداية",
        "tr": "Başlangıç"
    },
    "Cultivating the first premium saffron and pistachio farms with a dedication to organic and traditional farming methods.": {
        "fa": "کشت اولین مزارع زعفران و پسته ممتاز با تعهد به روش‌های کشاورزی ارگانیک و سنتی.",
        "ar": "زراعة أولى مزارع الزعفران والفستق الفاخرة مع الالتزام بأساليب الزراعة العضوية والتقليدية.",
        "tr": "Organik ve geleneksel tarım yöntemlerine bağlılıkla ilk birinci sınıf safran ve fıstık çiftliklerini yetiştirmek."
    },
    "Meet": {
        "fa": "ملاقات",
        "ar": "تعرف على",
        "tr": "Tanışın"
    },
    "Our Team": {
        "fa": "تیم ما",
        "ar": "فريقنا",
        "tr": "Ekibimiz"
    },
    "The dedicated experts behind the success of Palace Karimi.": {
        "fa": "کارشناسان متعهدی که پشت موفقیت پالاس کریمی هستند.",
        "ar": "الخبراء المتفانون وراء نجاح قصر كريمي.",
        "tr": "Palace Karimi'nin başarısının arkasındaki özverili uzmanlar."
    },
    "Abolfazl Karimi": {
        "fa": "ابوالفضل کریمی",
        "ar": "أبو الفضل كريمي",
        "tr": "Abolfazl Karimi"
    },
    "CEO & Founder": {
        "fa": "مدیرعامل و بنیان‌گذار",
        "ar": "الرئيس التنفيذي والمؤسس",
        "tr": "CEO ve Kurucu"
    },
    "Leading the global strategy and ensuring the highest quality standards across all products.": {
        "fa": "رهبری استراتژی جهانی و تضمین بالاترین استانداردهای کیفیت در تمام محصولات.",
        "ar": "قيادة الاستراتيجية العالمية وضمان أعلى معايير الجودة في جميع المنتجات.",
        "tr": "Küresel stratejiyi yönetmek ve tüm ürünlerde en yüksek kalite standartlarını sağlamak."
    },
    "Sara Ahmadi": {
        "fa": "سارا احمدی",
        "ar": "سارة أحمدي",
        "tr": "Sara Ahmadi"
    },
    "Export Manager": {
        "fa": "مدیر صادرات",
        "ar": "مديرة التصدير",
        "tr": "İhracat Müdürü"
    },
    "Managing international logistics, B2B relations, and smooth customs clearances.": {
        "fa": "مدیریت لجستیک بین‌المللی، روابط B2B و ترخیص کالا بدون مشکل.",
        "ar": "إدارة الخدمات اللوجستية الدولية وعلاقات B2B والتخليص الجمركي السلس.",
        "tr": "Uluslararası lojistik, B2B ilişkileri ve sorunsuz gümrük işlemlerini yönetmek."
    },
    "Ali Rezaei": {
        "fa": "علی رضایی",
        "ar": "علي رضائي",
        "tr": "Ali Rezaei"
    },
    "Quality Control": {
        "fa": "کنترل کیفیت",
        "ar": "مراقبة الجودة",
        "tr": "Kalite Kontrol"
    },
    "Mina Rostami": {
        "fa": "مینا رستمی",
        "ar": "مينا رستمي",
        "tr": "Mina Rostami"
    },
    "Marketing": {
        "fa": "بازاریابی",
        "ar": "التسويق",
        "tr": "Pazarlama"
    },
    "Showcasing the true value and luxury of Persian saffron to our international audience.": {
        "fa": "نمایش ارزش واقعی و لوکس بودن زعفران ایرانی به مخاطبان بین‌المللی.",
        "ar": "عرض القيمة الحقيقية والفخامة للزعفران الفارسي لجمهورنا الدولي.",
        "tr": "Uluslararası izleyicimize İran safranının gerçek değerini ve lüksünü sunmak."
    },
    "Palace Karimi; The Symbol of": {
        "fa": "پالاس کریمی؛ نماد",
        "ar": "قصر كريمي؛ رمز",
        "tr": "Palace Karimi; Sembolü"
    },
    "Authenticity": {
        "fa": "اصالت",
        "ar": "الأصالة",
        "tr": "Orijinallik"
    },
    "Join Our Network": {
        "fa": "به شبکه ما بپیوندید",
        "ar": "انضم إلى شبكتنا",
        "tr": "Ağımıza Katılın"
    },
    "International": {
        "fa": "بین‌المللی",
        "ar": "دولي",
        "tr": "Uluslararası"
    },
    "Certifications & Standards": {
        "fa": "گواهینامه‌ها و استانداردها",
        "ar": "الشهادات والمعايير",
        "tr": "Sertifikalar ve Standartlar"
    },
    "Committed to global food safety, organic farming, and premium export quality.": {
        "fa": "متعهد به ایمنی جهانی غذا، کشاورزی ارگانیک و کیفیت صادراتی ممتاز.",
        "ar": "ملتزمون بسلامة الأغذية العالمية والزراعة العضوية وجودة التصدير الممتازة.",
        "tr": "Küresel gıda güvenliği, organik tarım ve birinci sınıf ihracat kalitesine bağlıyız."
    },
    "With a rich heritage in cultivating the world’s finest saffron and pistachios, Palace Karimi stands as a bridge between the ancient farms of Persia and the luxury global market.": {
        "fa": "پالاس کریمی با میراثی غنی در کشت بهترین زعفران و پسته جهان، به‌عنوان پلی بین مزارع باستانی ایران و بازار لوکس جهانی ایستاده است.",
        "ar": "بإرث غني في زراعة أجود أنواع الزعفران والفستق في العالم، تقف قصر كريمي كجسر بين المزارع العريقة في فارس والسوق العالمية الفاخرة.",
        "tr": "Dünyanın en iyi safran ve fıstıklarını yetiştirme konusundaki zengin mirasıyla Palace Karimi, İran'ın kadim çiftlikleri ile lüks küresel pazar arasında bir köprü görevi görmektedir."
    },
    "We deliver nothing but perfection.": {
        "fa": "ما چیزی جز کمال ارائه نمی‌دهیم.",
        "ar": "نحن لا نقدم سوى الكمال.",
        "tr": "Kusursuzluktan başka bir şey sunmuyoruz."
    },
    "Overseeing laboratory testing and ensuring 100 Percent organic certification compliance.": {
        "fa": "نظارت بر آزمایش‌های آزمایشگاهی و اطمینان از انطباق ۱۰۰٪ گواهی ارگانیک.",
        "ar": "الإشراف على الاختبارات المخبرية وضمان الامتثال للشهادة العضوية بنسبة ۱۰۰٪.",
        "tr": "Laboratuvar testlerini denetlemek ve %100 organik sertifika uyumluluğunu sağlamak."
    },
    "Implementation of state-of-the-art sorting and packaging facilities to maintain 100 Percent purity and aroma.": {
        "fa": "پیاده‌سازی تجهیزات پیشرفته تفکیک و بسته‌بندی برای حفظ ۱۰۰٪ خلوص و عطر.",
        "ar": "تنفيذ مرافق فرز وتغليف حديثة للحفاظ على النقاء والرائحة بنسبة ۱۰۰٪.",
        "tr": "%100 saflık ve aromayı korumak için en son teknoloji ayıklama ve paketleme tesislerinin uygulanması."
    },
    "Our mission is to empower local farmers through fair trade while delivering 100 Percent organic, lab-tested, and exquisitely packaged products to our B2B partners and consumers worldwide.": {
        "fa": "ماموریت ما توانمندسازی کشاورزان محلی از طریق تجارت منصفانه و ارائه محصولات ۱۰۰٪ ارگانیک، آزمایش‌شده در آزمایشگاه و بسته‌بندی نفیس به شرکای B2B و مصرف‌کنندگان در سراسر جهان است.",
        "ar": "مهمتنا هي تمكين المزارعين المحليين من خلال التجارة العادلة مع تقديم منتجات عضوية ۱۰۰٪ ومختبرة مخبريًا ومعبأة بشكل رائع لشركائنا B2B والمستهلكين حول العالم.",
        "tr": "Misyonumuz, adil ticaret yoluyla yerel çiftçileri güçlendirirken, dünya çapındaki B2B ortaklarımıza ve tüketicilere %100 organik, laboratuvar testli ve zarif paketlenmiş ürünler sunmaktır."
    },
    "We guarantee that all our saffron and pistachios are 100 Percent authentic Persian products, free from any artificial additives or coloring.": {
        "fa": "ما تضمین می‌کنیم که تمام زعفران و پسته ما محصولات ۱۰۰٪ اصیل ایرانی، عاری از هرگونه افزودنی یا رنگ مصنوعی هستند.",
        "ar": "نضمن أن جميع منتجاتنا من الزعفران والفستق هي منتجات فارسية أصيلة ۱۰۰٪ وخالية من أي إضافات أو ألوان صناعية.",
        "tr": "Tüm safran ve fıstıklarımızın %100 orijinal İran ürünü olduğunu, hiçbir yapay katkı veya renklendirici içermediğini garanti ediyoruz."
    },
    "100 Percent Organic": {
        "fa": "۱۰۰٪ ارگانیک",
        "ar": "۱۰۰٪ عضوي",
        "tr": "%100 Organik"
    },
    "100 Percent Natural & Additive-Free": {
        "fa": "۱۰۰٪ طبیعی و بدون افزودنی",
        "ar": "۱۰۰٪ طبيعي وخالٍ من الإضافات",
        "tr": "%100 Doğal ve Katkısız"
    },
    "Fast and reliable international shipping to global destinations.": {
        "fa": "ارسال بین‌المللی سریع و مطمئن به مقاصد جهانی.",
        "ar": "شحن دولي سريع وموثوق إلى الوجهات العالمية.",
        "tr": "Küresel varış noktalarına hızlı ve güvenilir uluslararası kargo."
    },
    "Contact": {
        "fa": "تماس",
        "ar": "اتصال",
        "tr": "İletişim"
    },
    "We are here to answer your questions and discuss global export opportunities.": {
        "fa": "ما اینجا هستیم تا به سوالات شما پاسخ دهیم و فرصت‌های صادرات جهانی را بررسی کنیم.",
        "ar": "نحن هنا للإجابة على أسئلتكم ومناقشة فرص التصدير العالمية.",
        "tr": "Sorularınızı yanıtlamak ve küresel ihracat fırsatlarını görüşmek için buradayız."
    },
    "Error!": {
        "fa": "خطا!",
        "ar": "خطأ!",
        "tr": "Hata!"
    },
    "There was an error sending your message. Please check the fields.": {
        "fa": "هنگام ارسال پیام خطایی رخ داد. لطفاً فیلدها را بررسی کنید.",
        "ar": "حدث خطأ أثناء إرسال رسالتك. يرجى التحقق من الحقول.",
        "tr": "Mesajınız gönderilirken bir hata oluştu. Lütfen alanları kontrol edin."
    },
    "Your message has been sent to us.": {
        "fa": "پیام شما برای ما ارسال شد.",
        "ar": "تم إرسال رسالتك إلينا.",
        "tr": "Mesajınız bize gönderildi."
    },
    "Full Name": {
        "fa": "نام کامل",
        "ar": "الاسم الكامل",
        "tr": "Tam Ad"
    },
    "Subject": {
        "fa": "موضوع",
        "ar": "الموضوع",
        "tr": "Konu"
    },
    "Message": {
        "fa": "پیام",
        "ar": "الرسالة",
        "tr": "Mesaj"
    },
    "Send Message": {
        "fa": "ارسال پیام",
        "ar": "إرسال الرسالة",
        "tr": "Mesaj Gönder"
    },
    "Office": {
        "fa": "دفتر",
        "ar": "المكتب",
        "tr": "Ofis"
    },
    "Address:": {
        "fa": "آدرس:",
        "ar": "العنوان:",
        "tr": "Adres:"
    },
    "Phone:": {
        "fa": "تلفن:",
        "ar": "الهاتف:",
        "tr": "Telefon:"
    },
    "Email:": {
        "fa": "ایمیل:",
        "ar": "البريد الإلكتروني:",
        "tr": "E-posta:"
    },
    "Business": {
        "fa": "کسب‌وکار",
        "ar": "العمل",
        "tr": "İşletme"
    },
    "Hours": {
        "fa": "ساعات کاری",
        "ar": "ساعات العمل",
        "tr": "Çalışma Saatleri"
    },
    "Saturday to Wednesday - 9:00 AM to 5:00 PM": {
        "fa": "شنبه تا چهارشنبه - ۹ صبح تا ۵ عصر",
        "ar": "السبت إلى الأربعاء - ۹ صباحًا حتى ۵ مساءً",
        "tr": "Cumartesi - Çarşamba 09:00 - 17:00"
    },
    "Thursday - 9:00 AM to 2:00 PM": {
        "fa": "پنجشنبه - ۹ صبح تا ۲ بعدازظهر",
        "ar": "الخميس - ۹ صباحًا حتى ۲ ظهرًا",
        "tr": "Perşembe 09:00 - 14:00"
    },
    "Friday - Closed": {
        "fa": "جمعه - تعطیل",
        "ar": "الجمعة - مغلق",
        "tr": "Cuma - Kapalı"
    },
    "Whether you are looking for bulk saffron orders, premium pistachio exports, or white-labeling services, our experts are ready to assist you.": {
        "fa": "چه به دنبال سفارش عمده زعفران، صادرات پسته ممتاز یا خدمات برچسب اختصاصی باشید، کارشناسان ما آماده کمک به شما هستند.",
        "ar": "سواء كنت تبحث عن طلبات زعفران بالجملة، أو تصدير الفستق الممتاز، أو خدمات العلامة التجارية الخاصة، فإن خبراءنا مستعدون لمساعدتك.",
        "tr": "İster toplu safran siparişleri, ister birinci sınıf fıstık ihracatı, ister özel etiketleme hizmetleri arıyor olun, uzmanlarımız size yardımcı olmaya hazırdır."
    },
    "Palace Karimi is": {
        "fa": "پالاس کریمی است",
        "ar": "قصر كريمي هي",
        "tr": "Palace Karimi"
    },
    "Everything": {
        "fa": "همه چیز",
        "ar": "كل شيء",
        "tr": "Her Şey"
    },
    "you need for a": {
        "fa": "که برای یک",
        "ar": "التي تحتاجها لتجربة",
        "tr": "ihtiyacınız olan"
    },
    "Luxury": {
        "fa": "لوکس",
        "ar": "فاخرة",
        "tr": "Lüks"
    },
    "export experience!": {
        "fa": "تجربه صادراتی نیاز دارید!",
        "ar": "تصدير فاخرة!",
        "tr": "ihracat deneyimi!"
    },
    "The Best": {
        "fa": "بهترین",
        "ar": "الأفضل",
        "tr": "En İyi"
    },
    "choice for authentic Persian products.": {
        "fa": "انتخاب برای محصولات اصیل ایرانی.",
        "ar": "خيار للمنتجات الفارسية الأصيلة.",
        "tr": "otantik İran ürünleri için seçim."
    },
    "Hossein Karimi Trading": {
        "fa": "تجارت حسین کریمی",
        "ar": "تجارة حسين كريمي",
        "tr": "Hossein Karimi Trading"
    },
    "Palace Karimi Office": {
        "fa": "دفتر پالاس کریمی",
        "ar": "مكتب قصر كريمي",
        "tr": "Palace Karimi Ofisi"
    },
    "With years of experience in cultivation, processing, and exporting the finest Iranian saffron and pistachio, we offer quality and authenticity to global markets. All our products are packaged and shipped with international standards.": {
        "fa": "با سال‌ها تجربه در کشت، فرآوری و صادرات بهترین زعفران و پسته ایران، کیفیت و اصالت را به بازارهای جهانی عرضه می‌کنیم. تمام محصولات ما با استانداردهای بین‌المللی بسته‌بندی و ارسال می‌شوند.",
        "ar": "مع سنوات من الخبرة في زراعة ومعالجة وتصدير أجود أنواع الزعفران والفستق الإيراني، نقدم الجودة والأصالة للأسواق العالمية. جميع منتجاتنا معبأة ومشحونة وفق المعايير الدولية.",
        "tr": "En iyi İran safranı ve fıstığının yetiştirilmesi, işlenmesi ve ihracatı konusunda yılların deneyimiyle küresel pazarlara kalite ve orijinallik sunuyoruz. Tüm ürünlerimiz uluslararası standartlara uygun olarak paketlenir ve gönderilir."
    },
    "09303755667": {
        "fa": "۰۹۳۰۳۷۵۵۶۶۷",
        "ar": "۰۹۳۰۳۷۵۵۶۶۷",
        "tr": "09303755667"
    },
}


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def create_or_update_po(lang):
    po_path = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.po')
    ensure_dir(os.path.dirname(po_path))

    # اگر فایل از قبل وجود دارد، آن را بارگیری می‌کنیم؛ در غیر این صورت یک فایل جدید می‌سازیم
    if os.path.exists(po_path):
        po = polib.pofile(po_path)
    else:
        po = polib.POFile()

    # تنظیم متادیتا
    po.metadata = {
        'Project-Id-Version': '1.0',
        'Language': lang,
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }

    # پاک کردن همه ورودی‌های قبلی برای جلوگیری از تکرار
    po.clear()

    # افزودن همه رشته‌ها
    for msgid, trans_dict in TRANSLATIONS.items():
        if lang == 'en':
            msgstr = msgid
        else:
            msgstr = trans_dict.get(lang, '')
        entry = polib.POEntry(
            msgid=msgid,
            msgstr=msgstr
        )
        po.append(entry)

    po.save(po_path)
    print(f"Updated {po_path}")


if __name__ == '__main__':
    print("Starting translation generation...")
    for lang in LANGS:
        create_or_update_po(lang)
    print("Done. Now run: python manage.py compilemessages")