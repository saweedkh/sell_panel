# Third Party Packages
import re

from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
# Django Build-in
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

# Local Apps
from .models import TranslatorSetting


class TranslatorView(View):
    def post(self, request):
        try:
            if setting := TranslatorSetting.objects.get_default():
                html_tag_pattern = re.compile(r'<[^>]*>')
                source = setting.source_language
                targets_data: str = request.POST.get('targets')
                text = request.POST.get('text', '')
                context = {}
                targets = targets_data.split(',')
                targets = list(map(lambda x: x.replace('ns', 'zh-CN'), targets))
                if bool(html_tag_pattern.search(text)):
                    for target in targets:
                        translated = self.translate_html_content(
                            html_content=text,
                            target_language=target,
                            source=source,
                            engine=setting.search_engine
                        )
                        context[target] = translated
                else:
                    for target in targets:
                        translator = self.get_translator(setting.search_engine, source, target)
                        translated = translator.translate(text=text)
                        context[target] = translated

                if 'zh-CN' in context:
                    context['ns'] = context['zh-CN']
                    del context['zh-CN']
                return JsonResponse({'status': 200, 'context': context})
            else:
                raise RuntimeError("TranslatorSetting not found")

        except OperationalError as e:

            # Handle the case where the table does not exist
            return JsonResponse({'status': 500, 'message': _('پیکربندی ایجاد نشده است!')})
        except Exception as e:
            print('>>>', e)
            return JsonResponse({'status': 500, 'message': _('مشکلی در ترجمه خودکار وجود دارد')})

    @staticmethod
    def get_translator(search_engine, source, target):
        if search_engine == TranslatorSetting.GOOGLE:
            return GoogleTranslator(source=source, target=target)
        elif search_engine == TranslatorSetting.CHAT_GPT:
            pass
        elif search_engine == TranslatorSetting.MICROSOFT:
            pass
        else:
            return GoogleTranslator(source=source, target=target)

    def translate_html_content(self, html_content, target_language, source, engine):
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all text nodes within the HTML
        text_nodes = soup.find_all(text=True)

        # Translate each text node
        for node in text_nodes:
            if node.parent.name not in ['script', 'style']:
                # Exclude script and style tags from translation
                original_text = str(node)
                translator = self.get_translator(engine, source, target_language)
                translated = translator.translate(text=original_text)
                node.replace_with(translated)
        # Return the translated HTML content
        translated_html = str(soup)

        return translated_html
