def is_company_owner(request):
    is_owner = False
    if request.user.pk in request.user.company.get_owners:
        is_owner = True
    return {"is_company_owner": is_owner}
