# Django Built-in modules
from django.http.response import Http404

# Local apps
from .models import (
    Home,
    About,
)
from seo.models import AbstractBaseSeoModel


# Create or get default static pages

def get_or_create_home_page():
    """Get or create default home page record."""
    home_page = Home.objects.last()
    if not home_page:
        home_page = Home.objects.create(slug='/', page_display_status=AbstractBaseSeoModel.PUBLISH)
    else:
        if home_page.page_display_status != AbstractBaseSeoModel.PUBLISH:
            raise Http404
    return home_page


def get_or_create_about_us_page():
    """Get or create default about us page record."""
    about_us_page = About.objects.last()
    if not about_us_page:
        about_us_page = About.objects.create(slug='about-us', page_display_status=AbstractBaseSeoModel.PUBLISH)
    else:
        if about_us_page.page_display_status != AbstractBaseSeoModel.PUBLISH:
            raise Http404
    return about_us_page

