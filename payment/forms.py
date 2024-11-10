# Django Built-in modules
from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import Receipt, Card, PaymentSetting


# Admin #
class ReceiptInlineFormset(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            cd = form.cleaned_data
            if not cd.get('image') and not cd.get('tracking_code'):
                msg = _('عکس رسید و کد رهگیری نمیتواند با هم خالی باشد.')
                form.add_error('image', msg)
                form.add_error('tracking_code', msg)


class CardInlineFormset(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(CardInlineFormset, self).__init__(*args, **kwargs)
        self.queryset = Card.objects.has_active()  # automatically set enable card or none if any card exists

    def clean(self):
        for form in self.forms:
            cd = form.cleaned_data
            if not cd.get('account_number') and not cd.get('shaba') and not cd.get('card_number'):
                msg = ''
                form.add_error('card_number', msg)
                form.add_error('account_number', msg)
                form.add_error('shaba', msg)
                raise forms.ValidationError(_('حداقل یکی از مشخصات کارت لازم است.'))


class ReceiptAdminForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'

    def clean(self):
        cd = super().clean()
        if not cd.get('image') and not cd.get('tracking_code'):
            msg = _('عکس رسید و کد رهگیری نمیتواند با هم خالی باشد.')
            self.add_error('image', msg)
            self.add_error('tracking_code', msg)


class PaymentSettingAdminForm(forms.ModelForm):
    class Meta:
        model = PaymentSetting
        fields = '__all__'

    def clean_prepayment_percentage(self):
        prepayment_percentage = self.cleaned_data['prepayment_percentage']
        if 1 > prepayment_percentage < 100:
            raise forms.ValidationError(_('لطفا یک مقدار معتبر وارد کنید. (از ۱ تا ۱۰۰)'))
        return prepayment_percentage


# User-end #
class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(
                attrs={'class': 'upload-file form-control', 'required': True}
            )
        }
        labels = {
            'image': _('بارگذاری رسید')
        }
