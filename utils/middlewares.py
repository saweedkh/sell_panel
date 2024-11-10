from django.shortcuts import redirect
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.utils import translation
from django.utils.translation.trans_real import get_language_from_request
from django.urls import reverse


class RedirectToNonWww:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        host = request.META.get('HTTP_HOST')

        if host and host.startswith('www.'):
            non_www = host.replace('www.', '')
            scheme = 'https' if request.is_secure() else 'http'
            return redirect('{}://{}{}'.format(scheme, non_www, request.get_full_path()))

        return response


class RedirectToWww:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        host = request.META.get('HTTP_HOST')

        if host and not host.startswith('www.'):
            with_www = 'www.' + host
            scheme = 'https' if request.is_secure() else 'http'
            return redirect('{}://{}{}'.format(scheme, with_www, request.get_full_path()))

        return response


class RedirectToNewMediaStorage:
    old_storage_directory_path = '/wp-content/uploads/'
    new_storage__directory_path = settings.MEDIA_URL + 'content/'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        full_path = request.get_full_path()

        if full_path and full_path.startswith(self.old_storage_directory_path):
            scheme = 'https' if request.is_secure() else 'http'
            host = request.META.get('HTTP_HOST')
            full_path = full_path.replace(self.old_storage_directory_path, self.new_storage__directory_path)
            return redirect('{}://{}{}'.format(scheme, host, full_path))

        return response


class DefaultLanguageMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        try:
            lang = get_language_from_request(request=request, check_path=False)
            translation.activate(lang)
            if request.META.get('HTTP_ACCEPT_LANGUAGE'):
                del request.META['HTTP_ACCEPT_LANGUAGE']

        except Exception as e:
            translation.activate('fa')
