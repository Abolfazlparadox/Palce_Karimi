// این متغیر را در ابتدای تابع خود تعریف کن
const skinCssLink = document.getElementById('skin-css');
const htmlTag = document.documentElement;

// این بخش را دقیقا بعد از اینکه کاربر روی دکمه دارک/لایت کلیک کرد قرار بده:
if (htmlTag.classList.contains('dark')) {
    // سوئیچ به فایل پسته‌ای در حالت دارک مود
    skinCssLink.setAttribute('href', '/static/css/skins/default-dark.css');
} else {
    // بازگشت به فایل بنفش در حالت لایت مود
    skinCssLink.setAttribute('href', '/static/css/skins/default.css');
}