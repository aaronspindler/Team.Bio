from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from config.views import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("company/", include("companies.urls")),
    path("billing/", include("billing.urls")),
    path("system/health", health, name="system_health"),
    path("utils/", include("utils.urls")),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
