from django.urls import path

from companies.views import create_company, home, company_settings, remove_user, user_profile, edit_profile, \
    add_location, add_team, UpdateLocationView, UpdateTeamView

urlpatterns = [
    path("home", home, name="company_home"),
    path("settings", company_settings, name="company_settings"),
    path("create", create_company, name="create_company"),
    path("location/add", add_location, name="add_location"),
    path("location/<str:pk>/update", UpdateLocationView.as_view(), name="update_location"),
    path("team/add", add_team, name="add_team"),
    path("team/<str:pk>/update", UpdateTeamView.as_view(), name="update_team"),
    path("profile/<str:email_prefix>/remove", remove_user, name='remove_user'),
    path("profile/edit", edit_profile, name="edit_profile"),
    path("profile/<str:email_prefix>", user_profile, name="user_profile"),
]
