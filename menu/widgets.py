# Python Standard Lib
import json

# Django Built-in modules
from django.contrib.contenttypes.models import ContentType
from django.forms import Widget
from django.forms.renderers import get_default_renderer
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe


class GfkLookupWidget(Widget):
    template_name = 'menu/gfk_lookup_widget.html'

    def __init__(self, *args, **kwargs):
        self.ct_field_name = kwargs.pop('ct_field_name')
        self.parent_field = kwargs.pop('parent_field')
        super(GfkLookupWidget, self).__init__(*args, **kwargs)

    def create_urls(self):
        model = self.parent_field.model
        ct_field = model._meta.get_field(self.ct_field_name)
        choices = ct_field.get_choices()

        urls = dict()
        for type_id, type_name in choices:
            if not type_id:
                continue

            content_type = ContentType.objects.get_for_id(type_id)

            try:
                url = reverse(f'admin:{content_type.app_label}_{content_type.model}_changelist')
            except NoReverseMatch:
                continue

            urls[type_name] = url

        return urls

    def get_context(self, name, value, attrs):
        context = {
            'name': name,
            'value': value,
            'urls': json.dumps(self.create_urls()),
            'ct_field_name': self.ct_field_name,
        }
        return context

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ""

        context = self.get_context(name, value, attrs=None)
        return self._render(self.template_name, context, renderer)

    def _render(self, template_name, context, renderer=None):
        if renderer is None:
            renderer = get_default_renderer()
        return mark_safe(renderer.render(template_name, context))
