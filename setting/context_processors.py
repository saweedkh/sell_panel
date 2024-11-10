from setting.models import (
    SiteGlobalSetting,
    SocialMediaSetting,
)
from blog.models import AbstractBlogPost


def global_settings(request):
    _global_settings = SiteGlobalSetting.objects.last()
    if not _global_settings:
        _global_settings = SiteGlobalSetting.objects.create(name='Firefly')
    socials = SocialMediaSetting.objects.all()
    return {'global_settings': _global_settings, 'socials': socials}


def announcement_posts(request):
    _posts = AbstractBlogPost.objects.filter(announcement=True).published().order_by('-created')[:6]
    return {'announcement_posts': _posts}
