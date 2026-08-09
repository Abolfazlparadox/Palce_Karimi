import os
import polib

LOCALE_DIR = 'locale'

# دیکشنری جامع ترجمه‌های فوتر و هدر سایت
TRANSLATIONS = {
    # فوتر
    "Get in Touch": {
        "fa": "در ارتباط باشید",
        "ar": "ابق على تواصل",
        "tr": "İletişimde Kalın"
    },
    # هدر / breadcrumb
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
    # فروشگاه
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
    # صفحه جزئیات محصول
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
    # برند (در عنوان صفحات)
    "Palace Karimi": {
        "fa": "پالاس کریمی",
        "ar": "قصر كريمي",
        "tr": "Palace Karimi"
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