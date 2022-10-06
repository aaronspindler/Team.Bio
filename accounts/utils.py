from companies.models import Company


def attempt_connect_user_to_a_company(user):
    # Get user email root
    user_email_root = user.email_root
    # look for companies with url=email_root
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
