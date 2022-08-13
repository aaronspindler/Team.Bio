from django.urls import path

from companies.views import create_company, home

urlpatterns = [
    path("home", home, name="company_home"),
    path("create", create_company, name="create_company"),
]


