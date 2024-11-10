# Django Built-in Modules
from django import forms
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import MenuObject
from .widgets import GfkLookupWidget


class CustomMenuObjectModelForm(forms.ModelForm):
    class Meta:
        model = MenuObject
        fields = '__all__'
        widgets = {
            'object_id': GfkLookupWidget(
                ct_field_name='content_type',
                parent_field=MenuObject._meta.get_field('content_type'),
            )
        }

    def __init__(self, *args, **kwargs):
        super(CustomMenuObjectModelForm, self).__init__(*args, **kwargs)
        filtered_models = [
            ctype.id for ctype in ContentType.objects.all()
            if ctype.model_class() in admin.site._registry and hasattr(ctype.model_class(), 'get_absolute_url')
        ]
        self.fields['content_type'].queryset = ContentType.objects.filter(id__in=filtered_models)

    def clean(self):
        data = self.cleaned_data
        if not data.get('url') and not data.get('content_type'):
            raise ValidationError(_('لینک و شی مرتبط نمیتوانند با هم خالی باشند.'))

        return data

    def clean_object_id(self):
        data = self.cleaned_data
        if data.get('content_type'):
            if not data.get('object_id'):
                raise ValidationError(_('این فیلد لازم است.'))
            else:
                try:
                    model = data['content_type'].model_class()
                    model.objects.get(pk=data['object_id'])
                except model.DoesNotExist:
                    raise ValidationError(_('مقدار وارد شده مجاز نیست.'))

        return data['object_id']
