# Django Built-in
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.utils.translation import gettext_lazy as _

# Third-party apps
from adminsortable2.admin import CustomInlineFormSet


class RelatedPostInlineFormset(CustomInlineFormSet, BaseInlineFormSet):
    def clean(self):
        instance = self.instance

        if instance:
            for form in self.forms:
                cd = form.cleaned_data
                post = cd.get('to_post')

                if post and post == instance:
                    raise ValidationError(_('پست مرتبط نباید با خود محصول یکسان باشد.'))

            posts = [form.cleaned_data.get('to_post') for form in self.forms if form.cleaned_data.get('to_post')]
            if len(posts) != len(set(posts)):
                raise ValidationError(_('پست های مرتبط نباید تکراری باشند.'))
