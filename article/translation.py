# Local Apps
# Third Party Packages
from modeltranslation.translator import translator, TranslationOptions

from blog.translation import AbstractBlogCategoryTranslationOptions, AbstractBlogPostTranslationOptions, AbstractBlogTagTranslationOptions
from seo.translation import AbstractBaseSeoModelTranslationOptions
from .models import ArticlePost, ArticleTag, Category


class ArticlePostTranslationOptions(AbstractBlogPostTranslationOptions):
    fields = (
        *AbstractBlogPostTranslationOptions.fields,
        'premium_voice',
        'video_title',
        'premium_content',
        'media_text',
    )


class ArticleTagTranslationOptions(AbstractBlogTagTranslationOptions):
    pass



class ArticleCategoryTranslationOptions(AbstractBlogCategoryTranslationOptions):
    pass


translator.register(Category, ArticleCategoryTranslationOptions, )
translator.register(ArticlePost, ArticlePostTranslationOptions, )
translator.register(ArticleTag, ArticleTagTranslationOptions, )
