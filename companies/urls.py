from django.urls import path

from companies.views import (
    UpdateLocationView,
    UpdateTeamView,
    add_location,
    add_team,
    company_settings,
    create_company,
    delete_location,
    delete_team,
    edit_profile,
    home,
    invite,
    make_owner,
    remove_owner,
    remove_user,
    revoke_invite,
    user_profile,
)

urlpatterns = [
    path("home", home, name="company_home"),
    path("settings", company_settings, name="company_settings"),
    path("make-owner/<str:email_prefix>", make_owner, name="make_owner"),
    path("remove-owner/<str:email_prefix>", remove_owner, name="remove_owner"),
    path("revoke-invite/<str:email>", revoke_invite, name="revoke_invite"),
    path("create", create_company, name="create_company"),
    path("location/add", add_location, name="add_location"),
    path("location/<str:pk>/delete", delete_location, name="delete_location"),
    path(
        "location/<str:pk>/update", UpdateLocationView.as_view(), name="update_location"
    ),
    path("team/add", add_team, name="add_team"),
    path("team/<str:pk>/delete", delete_team, name="delete_team"),
    path("team/<str:pk>/update", UpdateTeamView.as_view(), name="update_team"),
    path("profile/<str:email_prefix>/remove", remove_user, name="remove_user"),
    path("profile/edit", edit_profile, name="edit_profile"),
    path("profile/<str:email_prefix>", user_profile, name="user_profile"),
    path("invite", invite, name="invite"),
]
