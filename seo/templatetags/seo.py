# Django Built-in modules
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.conf import settings
from django import template

# Python Standard Libraries
from typing import Dict
import json

# Google Schema Template Tag

DEFAULT_STRUCTURED_DATA = getattr(settings, 'DEFAULT_STRUCTURED_DATA', {})

_json_script_escapes = {
    ord('>'): '\u003E',
    ord('<'): '\u003C',
    ord('&'): '\u0026',
}


def json_encode(data: Dict) -> str:
    return json.dumps(data, cls=DjangoJSONEncoder, ensure_ascii=False).translate(_json_script_escapes)


def sub_defaults(data: Dict) -> Dict:
    data_out = {}
    for key, value in data.items():
        if value is None:
            data_out[key] = DEFAULT_STRUCTURED_DATA[key]
        else:
            data_out[key] = value

    return data_out


register = template.Library()


@register.simple_tag()
def schema(obj):
    if hasattr(obj, 'structured_data'):
        data = obj.structured_data

        encoded = json_encode(data)
        return format_html(
            '<script type="application/ld+json">{}</script>',
            mark_safe(encoded)
        )
    else:
        return ""
