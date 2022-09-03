from django.urls import path

from companies.views import create_company, home, company_admin

urlpatterns = [
    path("home", home, name="company_home"),
    path("admin", company_admin, name="company_admin"),
    path("create", create_company, name="create_company"),
]
