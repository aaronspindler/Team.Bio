from django.urls import path

from companies.views import create_company, home, company_settings

urlpatterns = [
    path("home", home, name="company_home"),
    path("settings", company_settings, name="company_settings"),
    path("create", create_company, name="create_company"),
]
