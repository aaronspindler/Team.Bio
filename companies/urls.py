from django.urls import path

from companies.views import (
    UpdateLocationView,
    UpdatePetView,
    UpdateTeamView,
    add_link,
    add_location,
    add_pet,
    add_team,
    company_settings,
    create_company,
    delete_link,
    delete_location,
    delete_pet,
    delete_team,
    edit_profile,
    home,
    invite,
    make_owner,
    pets,
    remove_owner,
    remove_user,
    revoke_invite,
    trivia,
    user_profile,
)

urlpatterns = [
    path("home", home, name="company_home"),
    # Administration
    path("create", create_company, name="create_company"),
    path("settings", company_settings, name="company_settings"),
    path("make-owner/<str:email_prefix>", make_owner, name="make_owner"),
    path("remove-owner/<str:email_prefix>", remove_owner, name="remove_owner"),
    path("revoke-invite/<str:email>", revoke_invite, name="revoke_invite"),
    path("invite", invite, name="invite"),
    # Locations
    path("location/add", add_location, name="add_location"),
    path("location/<str:pk>/delete", delete_location, name="delete_location"),
    path("location/<str:pk>/update", UpdateLocationView.as_view(), name="update_location"),
    # Teams
    path("team/add", add_team, name="add_team"),
    path("team/<str:pk>/delete", delete_team, name="delete_team"),
    path("team/<str:pk>/update", UpdateTeamView.as_view(), name="update_team"),
    # Links
    path("link/add", add_link, name="add_link"),
    path("link/<str:pk>/delete", delete_link, name="delete_link"),
    # Profiles
    path("profile/<str:email_prefix>/remove", remove_user, name="remove_user"),
    path("profile/edit", edit_profile, name="edit_profile"),
    path("profile/<str:email_prefix>", user_profile, name="user_profile"),
    # Pets
    path("pets", pets, name="company_pets"),
    path("profile/pet/add", add_pet, name="add_pet"),
    path("profile/pet/<str:pk>/delete", delete_pet, name="delete_pet"),
    path("profile/pet/<str:pk>/update", UpdatePetView.as_view(), name="update_pet"),
    # Trivia
    path("trivia", trivia, name="company_trivia"),
]
