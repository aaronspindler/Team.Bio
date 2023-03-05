from django.conf import settings

from companies.models import Company, Invite


def attempt_connect_user_to_a_company(user):
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


def attempt_connect_user_with_invites(user):
    invites = Invite.objects.filter(email__iexact=user.email)
    if invites:
        invite = invites.first()
        company = invite.company
        user.company = company
        user.save()
        invite.delete()
        return True
    return False
