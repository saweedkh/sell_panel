# Django Built-in modules
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class PagesSitemap(Sitemap):
    priority = 0.6
    changefreq = 'never'
    protocol = "https"

    def items(self):
        return [
            'pages:home',
            'pages:about_us',
            'account:login',
            'account:user_register',
            'account:user_forgot_password',
        ]

    def location(self, item):
        if item == 'pages:home':
            self.priority = 1.0
            self.changefreq = 'weekly'
        else:
            self.priority = 0.6
            self.changefreq = 'never'
        return reverse(item)
