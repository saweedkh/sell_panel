# Django Built-in modules
from django import forms
from django.utils.translation import gettext_lazy as _

# Local apps
from .models import DiscountCoupon


class DiscountCouponAdminForm(forms.ModelForm):
    class Meta:
        model = DiscountCoupon
        fields = '__all__'

    def clean_amount(self):
        discount_type = self.cleaned_data.get('type')
        amount = self.cleaned_data.get('amount')

        if discount_type == DiscountCoupon.PERCENTAGE_DISCOUNT and not 1 <= amount <= 100:
            raise forms.ValidationError(_('مطمئن شوید این مقدار بین 1 تا 100 است.'))

        if amount <= 0:
            raise forms.ValidationError(_('مطمئن شوید این مقدار بزرگتر از 0 است.'))

        return amount
