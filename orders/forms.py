# Django Built-in modules
from django import forms
from django.forms.models import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _
from django.shortcuts import reverse
from django.contrib import messages
from django.utils.html import format_html
from django.utils.safestring import mark_safe

# Local Apps
from .models import Order, OrderItem
from account.models import UserAddress
from payment.models import PaymentSetting
from products.models import Warehouse

# Third-party apps
from phonenumber_field.formfields import PhoneNumberField


class OrderForm(forms.ModelForm):
    
    address_id = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect(),
        required=False,
    )
    payment_method = forms.ChoiceField(
        label=_('روش پرداخت'),
        required=True,
        widget=forms.RadioSelect(),
        error_messages={
            'required': _("لطفا شیوه پرداخت مدنظر خود را انتخاب کنید."),
        },
    )

    class Meta:
        model = Order
        authenticated_users_fields = ('address_id',)

        anonymous_users_fields = ('first_name', 'last_name', 'mobile_number', 'email', 'province_id', 'city_id',
                                  'address', 'postal_code',)

        general_fields = ('note', 'payment_method',)

        fields = authenticated_users_fields + anonymous_users_fields + general_fields
        labels = {
            'email': _('ایمیل (اختیاری)'),
            'postal_code': _('کد پستی (اختیاری)'),
            'note': _('یادداشت (اختیاری)'),
        }
        error_messages = {
            'first_name': {'required': _("لطفا نام خود را وارد کنید."), },
            'last_name': {'required': _("لطفا نام خانوادگی خود را وارد کنید."), },
            'mobile_number': {'required': _("لطفا شماره موبایل خود را وارد کنید."), },
            'province_id': {'required': _("لطفا استان خود را انتخاب کنید."), },
            'city_id': {'required': _("لطفا شهر خود را انتخاب کنید."), },
            'address': {'required': _("لطفا آدرس خود را وارد کنید."), },
        }
        widgets = {
            'postal_code': forms.NumberInput(),
            'province_id': forms.Select(
                attrs={
                    'placeholder': _('استان'),
                    'class': 'form-select',
                    'style': 'height: 57px; border: 1px white; background-color: #232323; border-radius: 0; color: white',
                    'required': True,
                    'id': 'id_province_id',
                    'name': 'province_id',
                },
            ),
            'city_id': forms.Select(
                attrs={
                    'placeholder': _('شهر'),
                    'class': 'form-select',
                    'style': 'height: 57px; border: 1px white; background-color: #232323; border-radius: 0; color: white',
                    'required': True,
                    'id': "id_city_id",
                    'name': 'city_id',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.cart = kwargs.pop('cart')
        self.user_is_authenticated = True if self.request.user.is_authenticated else False

        super(OrderForm, self).__init__(*args, **kwargs)

        if self.user_is_authenticated:
            self.fields['address_id'].queryset = Address.objects.filter(user=self.request.user)
            [self.fields.pop(field) for field in self.Meta.anonymous_users_fields]
        else:
            [self.fields.pop(field) for field in self.Meta.authenticated_users_fields]
            self.fields['province_id'].required = True
            self.fields['city_id'].required = True
            self.fields['province_id'].empty_label = _('استان خود را انتخاب کنید')
            self.fields['city_id'].empty_label = _('شهر خود را انتخاب کنید')


        payment_methods = PaymentSetting.objects.get_first().payment_status(
            user_is_authenticated=self.user_is_authenticated,
        )

        self.fields['payment_method'].choices = payment_methods
        if payment_methods:
            self.fields['payment_method'].initial = payment_methods[0][0]

    def clean_address_id(self):
        user = self.request.user
        selected_address = self.cleaned_data.get('address_id')
        if user.is_authenticated:
            if not user.addresses.exists():
                raise forms.ValidationError(
                    mark_safe(
                        _('ابتدا لطفا از طریق {} یا {}، یک آدرس جدید ایجاد کنید.'.format(
                            format_html(u'<b>{}</b>', _('دکمه افزودن آدرس')),
                            format_html(
                                u'<a target="_blank" href="{}">{}</a>',
                                reverse('account:address_add'), _('بخش آدرس ها')
                            ),
                        ))
                    )
                )

            if not selected_address:
                raise forms.ValidationError(_('لطفا یک آدرس را برای ارسال مرسوله انتخاب کنید.'))

            if not user.mobile_number and not selected_address.mobile_number:
                raise forms.ValidationError(
                    mark_safe(
                        _('لطفا شماره موبایل خود را در بخش {} یا در بخش {} وارد کنید.'.format(
                            format_html(
                                u'<a target="_blank" href="{}">{}</a>',
                                reverse('account:profile'), _('اطلاعات حساب')
                            ),
                            format_html(
                                u'<a target="_blank" href="{}">{}</a>',
                                selected_address.edit_absolute_url(), _('شماره موبایل گیرنده')
                            ),
                        ))
                    )
                )
        return selected_address

    def clean_payment_method(self):
        selected_payment_method = self.cleaned_data.get('payment_method')

        if int(selected_payment_method) == Order.WALLET and self.request.user.is_authenticated:
            wallet = self.request.user.wallet
            left_money = self.cart.total - wallet.balance
            if left_money > 0:
                raise forms.ValidationError(
                    mark_safe(
                        _('موجودی کیف پول شما کافی نیست. لطفا ابتدا از طریق {}، کیف پول خود را شارژ کنید یا روش پرداخت دیگری انتخاب کنید.'.format(
                            format_html(
                                u'<a target="_blank" href="{}">{}</a>',
                                self.request.user.wallet.charge_absolute_url(left_money), _('بخش شارژ کیف پول')),
                        )))
                )
        return selected_payment_method


class OrderItemAdminForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'
        # help_texts = {
        #     'variant': _('لطفا تنوع محصول را از لیست محصولات انتخاب کنید.')
        # }


class OrderItemInlineFormset(BaseInlineFormSet):
    def clean(self):
        for form in self.forms:
            cd = form.cleaned_data
            variant = cd.get('variant')
            variant_pk = cd.get('id')
            quantity = cd.get('quantity') if cd.get('quantity') else 0

            if quantity <= 0:
                raise forms.ValidationError(
                    _('تعداد باید عددی بزرگتر از ۰ باشد. (آیتم سفارش {})'.format(variant_pk))
                )

            if 'variant' in form.changed_data and form.instance and variant_pk and form.instance.variant_id != variant:
                raise forms.ValidationError(
                    _('شما نمی توانید تنوع محصول ثبت شده را تغییر دهید.(آیتم سفارش {}) لطفا یک سفارش دیگر ثبت کنید یا آیتم فعلی را حذف، و آیتم جدید ایجاد کنید.'.format(
                        variant_pk))
                )


class OrderTrackingForm(forms.Form):
    mobile_number = PhoneNumberField(
        label=_('شماره موبایل'),
        error_messages={'invalid': _('یک شماره موبایل معتبر وارد کنید.')},
        widget=forms.NumberInput(
            attrs={
                'placeholder': _('شماره موبایل خود را وارد کنید'),
                'style': "text-align: right; background-color: #232323; direction: rtl; border: 1px solid #232323",
            }
        ),
    )
    tracking_code = forms.CharField(
        label=_('کد ارجاع یا پیگیری'),
        widget=forms.NumberInput(
            attrs={
                'placeholder': _('کد ارجاع یا کد پیگیری سفارش خود را وارد کنید'),
                 'style': "text-align: right; background-color: #232323; border: 1px solid #232323",
            }
        ),
    )

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data['mobile_number']
        return str(mobile_number).replace(' ', '')

    def clean_tracking_code(self):
        tracking_code = self.cleaned_data['tracking_code']
        tracking_code_length = len(tracking_code)
        if tracking_code_length == 6 or tracking_code_length == 16:
            return tracking_code
        raise forms.ValidationError(_('لطفا یک کد معتبر وارد کنید.'))


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self._error_has_raised = False
        super().__init__(*args, **kwargs)

        try:
            self.fields['payment_method'].initial = Order.TRANSFER
        except Exception:
            pass

    def clean_order_status(self):
        new_status = self.cleaned_data['order_status']
        old_status = self.instance.order_status
        first_time_created = True if self.instance.pk is None else False
        self.instance.__last_order_status__ = old_status
        change_result, possible_statuses = self.instance.action_after_status_change(
            old_status=old_status,
            new_status=new_status,
            search_for_possible_status=True,
            first_time_create=first_time_created,
        )
        if change_result == Order.WAREHOUSE_FORBIDDEN:
            self._error_has_raised = True
            raise forms.ValidationError(
                _(f'تغییر وضعیت از حالت {Order.get_status_name([old_status])} به {Order.get_status_name([new_status])} مجاز نیست. حالت های ممکن: {Order.get_status_name(possible_statuses)}')
            )

        if old_status == Order.AWAITING_PAYMENT and new_status == Order.DOING:
            messages.warning(
                self.request,
                mark_safe(
                    _(f'در صورت اعمال تغییر در آیتم های سفارش یا تعداد آن ها، می توانید یک <a href="{self.instance.create_invoice_absolute_url()}" target="_blank">صورت حساب جدید</a> ایجاد کنید.')
                )
            )
        return new_status

    def clean_province_id(self):
        province = self.cleaned_data['province_id']
        if self._error_has_raised:
            return province

        order_status = self.cleaned_data['order_status']
        if order_status == Order.DOING and not province:
            raise forms.ValidationError(
                _('پر کردن فیلد استان اجباری است.')
            )
        return province

    def clean_city_id(self):
        city = self.cleaned_data['city_id']
        if self._error_has_raised:
            return city

        order_status = self.cleaned_data['order_status']
        if order_status == Order.DOING and not city:
            raise forms.ValidationError(
                _('پر کردن فیلد شهر اجباری است.')
            )
        return city

    def clean_packing_type(self):
        packing_type = self.cleaned_data['packing_type']
        if self._error_has_raised:
            return packing_type

        order_status = self.cleaned_data['order_status']
        if order_status == Order.PACKING and not packing_type:
            raise forms.ValidationError(
                _('پر کردن فیلد نوع بسته بندی اجباری است.')
            )
        return packing_type

    def clean_payment_method(self):
        payment_method = self.cleaned_data.get('payment_method')
        if not payment_method:
            raise forms.ValidationError(
                _(f'لطفا روش پرداخت را مشخص کنید.')
            )
        return payment_method
