from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PagesSitemap(Sitemap):
    def items(self):
        return [
            "home",
            "pricing",
            "account_signup",
            "account_login",
            "privacy_policy",
            "terms_of_service",
            "robotstxt",
        ]

    def location(self, item):
        return reverse(item)
