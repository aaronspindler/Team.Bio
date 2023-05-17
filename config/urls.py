from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from config.sitemaps import BlogSitemap, PagesSitemap
from config.views import health, robotstxt

sitemaps = {
    "pages": PagesSitemap,
    "blog": BlogSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("company/", include("companies.urls")),
    path("billing/", include("billing.urls")),
    path("system/health", health, name="system_health"),
    path("robots.txt", robotstxt, name="robotstxt"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}),
    path("utils/", include("utils.urls")),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
