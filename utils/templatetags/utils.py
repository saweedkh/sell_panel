# Django Built-in modules
from django import template
from django.contrib.contenttypes.models import ContentType

# Local Apps
from utils.jdatetime import (
    humanize_datetime,
    pretty_jalali_datetime_format,
    standard_jalali_datetime_format,
)

# Python Standard Library
import re
import json
from auditlog.models import LogEntry

# Third Party Packages
import auditlog.mixins

register = template.Library()


@register.filter(name='humanize_datetime')
def humanize_jdatetime_template_tag(instance):
    return humanize_datetime(instance)


@register.filter(name='pretty_jalali')
def pretty_jalali_datetime_template_tag(instance):
    return pretty_jalali_datetime_format(instance)


@register.filter(name='standard_jalali')
def standard_jalali_datetime_format_template_tag(instance):
    return standard_jalali_datetime_format(instance)


@register.filter(name='persian_numbers')
def persian_numbers_template_tag(english_number):
    persian_numbers = ("۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹")
    number = str(english_number).replace(' ', '').replace('-', '')
    return ''.join(persian_numbers[int(digit)] for digit in number)


@register.simple_tag(name='load_history', takes_context=True)
def load_history_template_tag(context, obj):
    return LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(obj).pk, object_id=obj.pk)


@register.simple_tag(name='change_table', takes_context=True)
def change_table_template_tag(context, obj):
    auditlog_mixin = auditlog.mixins.LogEntryAdminMixin()
    return auditlog_mixin.msg(obj=obj)
