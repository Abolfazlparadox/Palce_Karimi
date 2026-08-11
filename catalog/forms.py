from django import forms
from django.utils.html import strip_tags
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    # لایه ۲: تله عسل (Honeypot) - کاربر نمی‌بیند، ربات پر می‌کند
    phone_ext = forms.CharField(
        required=False,
        label="Phone Extension",
        widget=forms.TextInput(attrs={
            'class': 'd-none',  # با کلاس بوت‌استرپ از دید کاربر مخفی می‌شود
            'autocomplete': 'off',
            'tabindex': '-1'
        })
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    # لایه ۳: پاکسازی (Sanitization)
    def clean_name(self):
        return strip_tags(self.cleaned_data.get('name', ''))  # حذف تگ‌های HTML (جلوگیری از XSS)

    def clean_subject(self):
        return strip_tags(self.cleaned_data.get('subject', ''))

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        message = strip_tags(message)

        # لایه ۳: جلوگیری از پیام‌های بی‌معنی و کوتاه
        if len(message) < 20:
            raise ValidationError(_("Your message is too short. Please provide more details (minimum 20 characters)."))

        return message

    def clean(self):
        cleaned_data = super().clean()

        # بررسی تله عسل
        if cleaned_data.get('phone_ext'):
            raise ValidationError(_("Spam bot detected!"))

        return cleaned_data