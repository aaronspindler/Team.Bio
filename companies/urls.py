from django.urls import path

from companies.views import create_company, home, company_settings, remove_user, user_profile

urlpatterns = [
    path("home", home, name="company_home"),
    path("settings", company_settings, name="company_settings"),
    path("create", create_company, name="create_company"),
    path("user/<str:user_to_remove>/remove", remove_user, name='remove_user'),
    path("<str:email_prefix>", user_profile, name="user_profile"),
]
