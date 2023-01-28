from functools import wraps

from django.http import Http404

from companies.models import CompanyOwner


def is_company_owner(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if CompanyOwner.objects.filter(
            owner=request.user, company=request.user.company
        ).exists():
            return function(request, *args, **kwargs)
        else:
            raise Http404

    return wrap
