from django.apps import apps
from django.conf import settings

from companies.models import Company, Invite


def attempt_connect_user_to_a_company(user_pk):
    Users = apps.get_model(settings.AUTH_USER_MODEL)
    user = Users.objects.get(pk=user_pk)
    if user.company:
        return False
    user_email_root = user.email_root
    # Don't auto connect users to a company if their email root is one of the popular free emails
    if user_email_root in settings.BLACKLISTED_DOMAIN_ROOTS:
        return False
    companies = Company.objects.filter(url_root=user_email_root)
    # if only 1 company found, proceed
    if companies.count() == 1:
        # set the users company to the found company
        user.company = companies.first()
        user.save()
        return True
    # if no company found, just return false
    # urls are restricted to be unique so there cannot be multiple companies with the same URL root / url
    return False


def attempt_connect_user_with_invites(user_pk):
    Users = apps.get_model(settings.AUTH_USER_MODEL)
    user = Users.objects.get(pk=user_pk)
    invites = Invite.objects.filter(email__iexact=user.email)
    if invites:
        invite = invites.first()
        company = invite.company
        user.company = company
        user.save()
        invite.delete()
        return True
    return False


def merge_user(user_pk):
    Users = apps.get_model(settings.AUTH_USER_MODEL)
    user = Users.objects.get(pk=user_pk)
    email = user.email
    other_users = Users.objects.filter(email=email).exclude(pk=user_pk)
    if other_users:
        other_user = other_users.first()
        company = other_user.company
        fields_to_copy = [
            "short_bio",
            "title",
            "general_location",
            "team",
            "personality_type",
            "chinese_zodiac",
            "zodiac_sign",
            "favourite_food",
            "favourite_movie",
            "favourite_travel_destination",
            "linkedin",
            "twitter",
            "github",
            "address_1",
            "city",
            "prov_state",
            "postal_code",
            "country",
            "start_date",
        ]
        for field in fields_to_copy:
            setattr(user, field, getattr(other_user, field, None))

        other_user_pets = other_user.pets.all()
        if other_user_pets:
            for pet in other_user_pets:
                pet.owner = user
                pet.save()

        other_user_companies = other_user.companies.all()
        if other_user_companies:
            for other_user_company in other_user_companies:
                other_user_company.owner = user
                other_user_company.save()

        other_user.delete()
        user.company = company
        user.save()
