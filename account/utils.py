# Django Built-in modules
from django.utils.translation import gettext_lazy as _

# Local Apps
from .models import MobilePhoneVerify

# Python Standard Library
import datetime

# Third party packages
from ratelimit.decorators import ratelimit
from random import randint
import requests
import json


def authenticate_to_webservice(user_api_key='782f497e8feffa6f66bb55ff', secret_key='zhr13361336!!!'):
    payload = "{\r\n  \"UserApiKey\": \"782f497e8feffa6f66bb55ff\",\r\n  \"SecretKey\": \"zhr13361336!!!\"\r\n}"
    response = requests.request(
        method="POST",
        url='http://RestfulSms.com/api/Token',
        headers={
            'Content-Type': 'application/json'
        },
        data=payload
    )
    result = json.loads(response.text)
    if result.get('IsSuccessful'):
        return result.get('TokenKey')


SEND_SMS_IP_LIMIT = '1/2m'
WAIT_LIMIT_LIFTED = 15 * 60
RESEND_LIMIT = 2 * 60


@ratelimit(key='ip', rate=SEND_SMS_IP_LIMIT)
def send_verification_code(request, mobile_number):
    if getattr(request, 'limited', False):
        return {'status': 403, 'message': _('تعداد درخواست بیش از حد مجاز! لطفا دقایقی صبر و مجددا امتحان کنید.'),
                'waiting_time': WAIT_LIMIT_LIFTED}

    # Authenticate to sms.ir
    token = authenticate_to_webservice()
    if not token:
        return {'status': 500, 'message': _('هنگام ارسال پیامک خطایی رخ داد! لطفا دقایقی دیگر مجددا امتحان کنید.'),
                'waiting_time': WAIT_LIMIT_LIFTED}

    # Generate verification code
    verification_code = str(randint(1000, 9999))

    mobile_number_verify = MobilePhoneVerify.objects.filter(mobile_number=mobile_number)
    if mobile_number_verify.exists():
        delta = datetime.datetime.now().replace(tzinfo=None) - mobile_number_verify.first().updated.replace(tzinfo=None)
        if delta.seconds < RESEND_LIMIT:
            return {'status': 403, 'message': _('تعداد درخواست بیش از حد مجاز! لطفا دقایقی صبر و مجددا امتحان کنید.'),
                    'waiting_time': RESEND_LIMIT}

    # response = requests.request(
    #     method='POST',
    #     url='http://RestfulSms.com/api/VerificationCode',
    #     headers={
    #         'Content-Type': 'application/json',
    #         'x-sms-ir-secure-token': token
    #     },
    #     data="{\r\n   \"Code\": \"" + str(verification_code) + "\",\r\n   \"MobileNumber\": \"" + str(
    #         mobile_number) + "\"\r\n} ",
    # )
    # result = json.loads(response.text)


    result ={
        'IsSuccessful' : True,
    }
    if result.get('IsSuccessful'):

        try:
            obj = MobilePhoneVerify.objects.get(mobile_number=mobile_number)
            obj.code = verification_code
            obj.status = MobilePhoneVerify.USABLE
            obj.save()
        except MobilePhoneVerify.DoesNotExist:
            obj = MobilePhoneVerify.objects.create(mobile_number=mobile_number, code=verification_code)
        

        return {'status': 200, 'message': _(f'کد تایید برای شماره {mobile_number} پیامک شد.'),
                'waiting_time': WAIT_LIMIT_LIFTED}

    return {'status': 500, 'message': _('هنگام ارسال پیامک خطایی رخ داد! لطفا دقایقی دیگر مجددا امتحان کنید.')}
