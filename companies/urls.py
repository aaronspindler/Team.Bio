from django.urls import path

from companies.views import create_company, home, company_settings, remove_user, invite_user

urlpatterns = [
    path("home", home, name="company_home"),
    path("settings", company_settings, name="company_settings"),
    path("create", create_company, name="create_company"),
    path("invite", invite_user, name="invite_user"),
    path("user/<int:user_to_remove_pk>/remove", remove_user, name='remove_user'),
]
