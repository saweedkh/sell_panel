# Django Built-in modules
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.models import BaseInlineFormSet
from django.conf import settings

# Local apps
from .models import (
    Product,
    ProductComment as Comment,
    ProductSpecification,
    Attribute,
)
from comment.forms import AnonymousBaseCommentForm, AuthenticatedBaseCommentForm, AuthenticatedBaseReplyForm, \
    AnonymousBaseReplyForm

# Third-party apps
from adminsortable2.admin import CustomInlineFormSet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Hidden

# Python Standard Libraries
import collections
import json


# Admin Panel Forms
class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_attributes(self):
        cleaned_data = self.cleaned_data
        product_type = cleaned_data.get("type")
        attributes = cleaned_data.get("attributes")

        if product_type == Product.VARIABLE and not attributes:
            raise forms.ValidationError(_('تعریف ویژگی برای محصول متنوع الزامی است.'))

        self.instance.__attributes___ = attributes

        return attributes


class ProductSpecificationInlineFormSet(forms.models.BaseInlineFormSet):
    model = ProductSpecification

    def __init__(self, *args, **kwargs):
        super(ProductSpecificationInlineFormSet, self).__init__(*args, **kwargs)

        if self.request.GET.get('extra', None):
            specifications = self.instance.get_specifications() if self.instance.pk else []
            initial_values = [
                form['general_attribute'].initial for form in self.forms
                if form['general_attribute'].initial
            ]
            for form, data in zip(self.forms, specifications):
                attribute = data.attribute
                if attribute not in initial_values:
                    form['general_attribute'].initial = attribute

    def clean(self):
        attributes_list = list()

        for form in self.forms:
            cd = form.cleaned_data
            attribute = cd.get('general_attribute')
            attribute_values = cd.get('attribute_value')
            custom_attribute_value = cd.get('custom_attribute_value')

            if attribute:
                attributes_list.append(attribute)

            if not attribute_values and not custom_attribute_value:
                raise forms.ValidationError(_('مقدار و مقدار دلخواه ویژگی هردو نمی توانند خالی باشند.'))

            if attribute and attribute_values:
                for attribute_value in attribute_values:
                    if attribute_value.attribute_id != attribute.pk:
                        raise forms.ValidationError(
                            _(f"مقدار ویژگی {attribute_value.name} به ویژگی {attribute} مربوط نیست")
                        )

        if len(attributes_list) != len(set(attributes_list)):
            duplicated = [item for item, count in collections.Counter(attributes_list).items() if count > 1]
            duplicated_attributes_name = ', '.join([attr_name.name for attr_name in duplicated])
            raise forms.ValidationError(
                _("ویژگی '{}' تکراری تعریف شده است.".format(duplicated_attributes_name, ))
            )


class VariantInlineFormset(BaseInlineFormSet):

    def clean(self):
        product_type = self.instance.type
        product_attributes = self.instance.__attributes___

        if product_attributes:
            product_attribute_ids = list(product_attributes.values_list('id', 'name'))
        else:
            product_attribute_ids = None

        variants_attribute_values = list()
        count = 0

        for form in self.forms:
            cd = form.cleaned_data

            try:

                if cd.get('default'):
                    count += 1

            except AttributeError:
                pass

            if product_type == Product.VARIABLE and product_attribute_ids:
                attribute_values_qs = list(cd.get('attribute_values').values_list('id', 'name', 'attribute_id',
                                                                                  'attribute_name'))
                attributes = [(attr[2], attr[3]) for attr in attribute_values_qs]
                attribute_values = [(attr_value[0], attr_value[1]) for attr_value in attribute_values_qs]

                if not attribute_values:
                    raise forms.ValidationError(
                        _('پر کردن مقدار ویژگی برای محصول متنوع الزامی است. (تنوع محصول: {})'.format(cd.get('id')))
                    )
                for attr in attributes:

                    if attr[0] not in [product_attr_id[0] for product_attr_id in product_attribute_ids]:
                        raise forms.ValidationError(
                            _("'{}' برای تنوع محصول '{}' داخل ویژگی های محصول تعریف نشده است.".format(
                                attr[1], cd.get('id'))
                            )
                        )

                for product_attribute_id in product_attribute_ids:
                    if product_attribute_id[0] not in [attr[0] for attr in attributes]:
                        raise forms.ValidationError(
                            _("ویژگی '{}' برای متعیر محصول '{}' تعریف نشده است.".format(
                                product_attribute_id[1], cd.get('id'))
                            )
                        )

                if len(attributes) != len(set(attributes)):
                    duplicated = [item for item, count in collections.Counter(attributes).items() if count > 1]
                    duplicated_attributes_name = ', '.join([attr_name[1] for attr_name in duplicated])
                    raise forms.ValidationError(
                        _("ویژگی '{}'، برای تنوع محصول '{}' تکراری تعریف شده است.".format(
                            duplicated_attributes_name, cd.get('id'))
                        )
                    )

                if attribute_values in variants_attribute_values:
                    duplicated_attribute_values_name = ', '.join([attr_name[1] for attr_name in attribute_values])
                    raise forms.ValidationError(
                        _("تنوع محصول با این ویژگی ها({}) از قبل موجود است.({})".format(
                            duplicated_attribute_values_name, cd.get('id'))
                        )
                    )
                variants_attribute_values.append(attribute_values)

        if count < 1 and product_type == Product.SIMPLE:
            raise forms.ValidationError(_('یک تنوع را به عنوان تنوع پیشفرض انتخاب کنید.'))
        elif count > 1:
            raise forms.ValidationError(_('تنها می توانید یک تنوع را به عنوان تنوع پیشفرض انتخاب کنید.'))


class AttributeInlineFormset(CustomInlineFormSet, BaseInlineFormSet):

    def clean(self):
        attribute_name = self.data.get('name')
        if self.data.get('input_field_type') == str(Attribute.COLORED_RADIO_BUTTON):
            for form in self.forms:
                cd = form.cleaned_data
                if not cd.get('color'):
                    name = cd.get('name')
                    raise forms.ValidationError(
                        _(f'برای {attribute_name} \"{name}\" رنگی انتخاب نشده است.')
                    )
        elif self.data.get('input_field_type') == str(Attribute.PATTERNED_RADIO_BUTTON):
            for form in self.forms:
                cd = form.cleaned_data
                if not cd.get('pattern'):
                    name = cd.get('name')
                    raise forms.ValidationError(
                        _(f'برای {attribute_name} {name} طرحی انتخاب نشده است.')
                    )


# End Admin Panel Forms


class SelectAttributeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.all_attributes_and_values, self.variant_attributes_and_values, \
        self.attribute_values_colors_or_patterns = kwargs.pop('product_attributes')
        self.attributes_input_types = kwargs.pop('attributes_input_types')
        self.default_variant_pk = kwargs.pop('default_variant_pk')
        self.have_problem_in_variation = False

        super(SelectAttributeForm, self).__init__(*args, **kwargs)
        try:
            self.helper = FormHelper()
            self.helper.label_class = 'product-title fw-bold mb-2'
            # self.helper.field_class = 'select-packege form-floating theme-form-floating'
            self.helper.layout = Layout()
            color_dic = dict()
            pattern_dic = dict()

            if self.all_attributes_and_values and self.default_variant_pk:
                for attribute, values in self.all_attributes_and_values.items():
                    input_type = int(self.attributes_input_types.get(attribute[0]))
                    if input_type == Attribute.DROP_DOWN:
                        self.fields[f'attribute_{attribute[0]}'] = forms.ChoiceField(
                            initial=self.variant_attributes_and_values[self.default_variant_pk][attribute],
                            label=attribute[1],
                            choices=sorted(list(values), key=lambda tup: tup[1]),
                            widget=forms.Select(
                                attrs={'data-attribute-id': attribute[0],
                                       'style': 'background-color: #232323; color: #9d9a9a;'}
                            ),
                        )
                        self.helper.layout.append(Layout(Field(f'attribute_{attribute[0]}', css_class='form-select')))
                    else:
                        color_or_pattern = self.attribute_values_colors_or_patterns.get(attribute)

                        self.fields[f'attribute_{attribute[0]}'] = forms.ChoiceField(
                            initial=self.variant_attributes_and_values[self.default_variant_pk][attribute],
                            label=attribute[1],
                            choices=sorted(list(values), key=lambda tup: tup[1]),
                            widget=forms.RadioSelect(
                                attrs={
                                    'data-attribute-id': attribute[0],
                                }
                            ),
                        )
                        if input_type == Attribute.SIMPLE_RADIO_BUTTON:
                            self.helper.layout.append(
                                Layout(Div(Field(f'attribute_{attribute[0]}'), css_class='simple-radio'))
                            )

                        elif input_type == Attribute.COLORED_RADIO_BUTTON:
                            self.helper.layout.append(
                                Layout(Div(f'attribute_{attribute[0]}', css_class='radio-color-package'))
                            )
                            for (vid, color, pattern_url) in color_or_pattern:
                                color_dic[vid] = color

                        elif input_type == Attribute.PATTERNED_RADIO_BUTTON:
                            self.helper.layout.append(
                                Layout(Div(f'attribute_{attribute[0]}', css_class='radio-pattern-package'))
                            )
                            for (vid, color, pattern_url) in color_or_pattern:
                                pattern_dic[vid] = settings.MEDIA_URL + pattern_url

                self.helper.add_input(Hidden('variants-colors', json.dumps(color_dic)))
                self.helper.add_input(Hidden('variants-patterns', json.dumps(pattern_dic)))

        except Exception as error:
            self.have_problem_in_variation = True


class AnonymousCommentForm(AnonymousBaseCommentForm):
    class Meta:
        model = Comment
        # fields = ('name', 'email', 'review', 'captcha')
        fields = ('name', 'email', 'review',)


class AuthenticatedCommentForm(AuthenticatedBaseCommentForm):
    class Meta:
        model = Comment
        fields = ('review',)


class AnonymousReplyForm(AnonymousBaseReplyForm):
    class Meta:
        model = Comment
        # fields = ('name', 'email', 'review', 'parent', 'comment_type', 'captcha')
        fields = ('name', 'email', 'review', 'parent', 'comment_type',)


class AuthenticatedReplyForm(AuthenticatedBaseReplyForm):
    class Meta:
        model = Comment
        fields = ('review', 'parent', 'comment_type')


class RelatedProductInlineFormset(CustomInlineFormSet, BaseInlineFormSet):
    def clean(self):
        instance = self.instance

        if instance:
            for form in self.forms:
                cd = form.cleaned_data
                product = cd.get('to_product')

                if product and product == instance:
                    raise forms.ValidationError(_('محصول مرتبط نباید با خود محصول یکسان باشد.'))

            products = [form.cleaned_data.get('to_product') for form in self.forms if
                        form.cleaned_data.get('to_product')]

            if len(products) != len(set(products)):
                raise forms.ValidationError(_('محصولات مرتبط نباید تکراری باشند.'))
