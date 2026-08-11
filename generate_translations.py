import os
import polib

LOCALE_DIR = 'locale'

# دیکشنری جامع ترجمه‌های کامل سایت برای ۴ زبان (FA, AR, TR)
TRANSLATIONS = {
    # ---------------------------------------------------------------------------
    # پیام‌ها و اعلان‌های سیستم (Messages & Alerts)
    # ---------------------------------------------------------------------------
    "You have sent too many messages. Please try again later.": {
        "fa": "تعداد پیام‌های شما بیش از حد مجاز است. لطفاً بعداً دوباره تلاش کنید.",
        "ar": "لقد أرسلت عددًا كبيرًا جدًا من الرسائل. يرجى المحاولة مرة أخرى لاحقًا.",
        "tr": "Çok fazla mesaj gönderdiniz. Lütfen daha sonra tekrar deneyiniz."
    },
    "Your message has been sent successfully. We will contact you soon.": {
        "fa": "پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.",
        "ar": "تم ارسال رسالتك بنجاح. وسوف نتصل بك قريبا.",
        "tr": "Mesajınız başarıyla gönderildi. En kısa sürede sizinle iletişime geçeceğiz."
    },
    "success_contact": {
        "fa": "پیام شما با موفقیت ارسال شد. به زودی با شما تماس خواهیم گرفت.",
        "ar": "تم ارسال رسالتك بنجاح. وسوف نتصل بك قريبا.",
        "tr": "Mesajınız başarıyla gönderildi. En kısa sürede sizinle iletişime geçeceğiz."
    },
    "Too many requests. Please try again later.": {
        "fa": "تعداد درخواست‌ها بیش از حد مجاز است. لطفاً بعداً دوباره تلاش کنید.",
        "ar": "طلبات كثيرة جدا. يرجى المحاولة مرة أخرى لاحقًا.",
        "tr": "Çok fazla istek. Lütfen daha sonra tekrar deneyiniz."
    },
    "Please enter an email address.": {
        "fa": "لطفاً یک آدرس ایمیل وارد کنید.",
        "ar": "يرجى إدخال البريد الإلكتروني.",
        "tr": "Lütfen bir e-posta adresi girin."
    },
    "Thank you for subscribing to our newsletter.": {
        "fa": "با تشکر از عضویت شما در خبرنامه.",
        "ar": "شكرا لاشتراكك في نشرتنا الإخبارية.",
        "tr": "Bültenimize abone olduğunuz için teşekkür ederiz."
    },
    "You are already subscribed to our email list.": {
        "fa": "شما قبلاً در خبرنامه ثبت‌نام کرده‌اید.",
        "ar": "أنت مشترك بالفعل في قائمتنا البريدية.",
        "tr": "E-posta listemize zaten abonesiniz."
    },
    "Invalid email address. Please check and try again.": {
        "fa": "آدرس ایمیل نامعتبر است. لطفاً بررسی و دوباره تلاش کنید.",
        "ar": "عنوان بريد إلكتروني غير صالح. يرجى التحقق والمحاولة مرة أخرى.",
        "tr": "Geçersiz e-posta adresi. Lütfen kontrol edip tekrar deneyin."
    },

    # ---------------------------------------------------------------------------
    # اعتبارسنجی فرم‌ها (Form Validation)
    # ---------------------------------------------------------------------------
    "Your message is too short. Please provide more details (minimum 20 characters).": {
        "fa": "متن پیام شما بسیار کوتاه است. لطفاً اطلاعات بیشتری وارد کنید (حداقل ۲۰ کاراکتر).",
        "ar": "رسالتك قصيرة جداً. يرجى تقديم المزيد من التفاصيل (۲۰ حرفاً على الأقل).",
        "tr": "Mesajınız çok kısa. Lütfen daha fazla detay verin (en az 20 karakter)."
    },
    "Spam bot detected!": {
        "fa": "ربات اسپم شناسایی شد!",
        "ar": "تم اكتشاف برامج بريد عشوائي!",
        "tr": "Spam botu tespit edildi!"
    },
    "Phone Extension": {
        "fa": "پیش‌شماره تلفن",
        "ar": "تحويلة الهاتف",
        "tr": "Dahili Telefon"
    },

    # ---------------------------------------------------------------------------
    # هدر، فوتر و ناوبری (Header, Footer & Navigation)
    # ---------------------------------------------------------------------------
    "Get in Touch": {
        "fa": "در ارتباط باشید",
        "ar": "ابق على تواصل",
        "tr": "İletيشimde Kalın"
    },
    "Home": {
        "fa": "خانه",
        "ar": "الرئيسية",
        "tr": "Ana Sayfa"
    },
    "Products": {
        "fa": "محصولات",
        "ar": "المنتجات",
        "tr": "Ürünler"
    },
    "Notifications": {
        "fa": "اعلان‌ها",
        "ar": "الإشعارات",
        "tr": "Bildirimler"
    },

    # ---------------------------------------------------------------------------
    # کاتالوگ و فروشگاه (Catalog & Shop)
    # ---------------------------------------------------------------------------
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

    # ---------------------------------------------------------------------------
    # برند و عناوین عمومی (Brand & Page Titles)
    # ---------------------------------------------------------------------------
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