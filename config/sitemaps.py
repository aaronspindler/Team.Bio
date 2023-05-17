from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from pages.models import BlogPost


class PagesSitemap(Sitemap):
    def items(self):
        return [
            "home",
            "pricing",
            "account_signup",
            "blog",
            "account_login",
            "privacy_policy",
            "terms_of_service",
            "robotstxt",
        ]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    def items(self):
        return BlogPost.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.edited_at
