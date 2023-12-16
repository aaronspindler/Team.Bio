def is_company_owner(request):
    is_owner = False
    user = request.user
    if user.is_authenticated and user.company and user.pk in user.company.get_owners:
        is_owner = True
    return {"is_company_owner": is_owner}
