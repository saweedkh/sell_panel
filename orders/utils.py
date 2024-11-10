# Python Standard Library
import json

# Third Party Packages
from auditlog.models import LogEntry
from auditlog.diff import model_instance_diff
from user_agents import parse

from datetime import datetime


def get_user_agent(request):
    ua_string = request.META['HTTP_USER_AGENT']
    user_agent = parse(ua_string)
    ua = {
        'ua_string': str(user_agent),

        'is_mobile': user_agent.is_mobile,
        'is_tablet': user_agent.is_tablet,
        'is_pc': user_agent.is_pc,
        'is_touch_capable': user_agent.is_touch_capable,
        'is_bot': user_agent.is_bot,
        'is_email_client': user_agent.is_email_client,

        # Device Information
        'device_brand': user_agent.device.brand,
        'device_family': user_agent.device.family,
        'device_model': user_agent.device.model,

        # Browser Information
        'browser_family': user_agent.browser.family,
        'browser_version': user_agent.browser.version_string,

        # OS Information
        'os_family': user_agent.os.family,
        'os_version': user_agent.os.version_string,
    }

    return ua


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def change_orders_status(queryset, status):
    old_qs = []
    for obj in queryset:
        old_qs.append(obj)

    queryset.update(order_status=status, updated=datetime.now())

    for old, new in zip(old_qs, queryset):
        changes = model_instance_diff(old, new)
        if changes:
            LogEntry.objects.log_create(
                new,
                action=LogEntry.Action.UPDATE,
                changes=json.dumps(changes),
            )
