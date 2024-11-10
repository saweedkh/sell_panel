# Django Built-in modules
from django.apps import apps

# Python Standard Library
import json
from urllib import parse
import uuid

# Local Apps
from . import default_settings


def get_json(resp):
    """
    :param response:returned response as json when sending a request
    using 'requests' module.

    :return:response's content with json format
    """

    return json.loads(resp.content.decode('utf-8'))


def append_querystring(url: str, params: dict) -> str:
    url_parts = list(parse.urlparse(url))
    query = dict(parse.parse_qsl(url_parts[4]))
    query.update(params)

    url_parts[4] = parse.urlencode(query)

    return parse.urlunparse(url_parts)


def split_to_dict_querystring(url: str) -> (str, dict):
    url_parts = list(parse.urlparse(url))
    query = dict(parse.parse_qsl(url_parts[4]))

    url_parts[4] = ''
    url_parts[5] = ''

    return parse.urlunparse(url_parts), query


def generate_tracking_code():
    return int(str(uuid.uuid4().int)[-1 * default_settings.TRACKING_CODE_LENGTH:])


def generate_reference_code():
    reference_code = int(str(uuid.uuid4().int)[-1 * 6:])
    Order = apps.get_model('orders', 'Order')
    if Order.objects.filter(reference_code=reference_code).exists():
        reference_code = generate_reference_code()
    return reference_code
