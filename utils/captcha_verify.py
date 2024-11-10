from datetime import datetime, timezone

from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from rest_framework import status
from rest_framework.response import Response


def verify(request, ser_data):
    # Verify the CAPTCHA
    captcha = request.data.get('captcha', None)
    captcha_hash_key = request.data.get('key', None)
    captcha_response: CaptchaStore = CaptchaStore.objects.filter(hashkey=captcha_hash_key).first()
    if not captcha:
        print('not captcha')
        return Response({'captcha': 'Captcha is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if captcha_response is None:
        print('not response')
        return Response({'captcha': 'Captcha verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if captcha != captcha_response.response:
            print('! response')
            return Response({'captcha': 'Captcha verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
        if (captcha_response.expiration.minute - datetime.now(timezone.utc).minute) <= 0:
            print('expired')
            CaptchaStore.delete(captcha_response)
            return Response({'captcha': 'Captcha verification failed.'}, status=status.HTTP_400_BAD_REQUEST)
    ser_data.create(ser_data.validated_data)
    CaptchaStore.delete(captcha_response)
    return Response('created successfully', status=status.HTTP_201_CREATED)


def get_captcha():
    new_captcha: CaptchaStore = CaptchaStore.generate_key()
    captcha_image_urls = captcha_image_url(new_captcha)
    return Response({'key': new_captcha, 'image_url': captcha_image_urls})
