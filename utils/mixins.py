# Django Built-in modules
from django.conf import settings

# Third Party Packages
from rest_framework.fields import empty


class SerializerTranslationMixin:
    """Show just translation fields"""

    def __init__(self, instance=None, data=empty, **kwargs):
        if not self.Meta.model_translation:
            raise AttributeError('You must define Meta.model_translation attribute')

        super().__init__(instance=instance, data=data, **kwargs)

    def get_field_names(self, declared_fields, info):
        fields = list(super().get_field_names(declared_fields, info))
        if not settings.USE_MULTI_LANGUAGE_FIELDS:
            return fields
        model_translation_fields = self.Meta.model_translation.fields
        languages = [lang[0] for lang in settings.LANGUAGES]
        for model_translation_field in model_translation_fields:
            if model_translation_field in fields:
                pos = fields.index(model_translation_field)
                fields[pos:pos + 1] = [f"{model_translation_field}_{lang}" for lang in languages]
        return fields
#
#
# class SerializerTranslationMixin:
#     """Show just serializer fields"""
#
#     def __init__(self, instance=None, data=empty, **kwargs):
#         super().__init__(instance=instance, data=data, **kwargs)


# class SerializerTranslationMixin:
#     """Show both of  serializer translation  fields"""
#
#     def __init__(self, instance=None, data=empty, **kwargs):
#         if not self.Meta.model_translation:
#             raise AttributeError('You must define Meta.model_translation attribute')
#
#         super().__init__(instance=instance, data=data, **kwargs)
#
#     def get_field_names(self, declared_fields, info):
#         fields = list(super().get_field_names(declared_fields, info))
#         model_translation_fields = self.Meta.model_translation.fields
#         languages = [lang[0] for lang in settings.LANGUAGES]
#         for model_translation_field in model_translation_fields:
#             if model_translation_field in fields:
#                 pos = fields.index(model_translation_field)
#                 for f in [f"{model_translation_field}_{lang}" for lang in languages]:
#                     fields.insert(pos + 1, f)
#         return fields
