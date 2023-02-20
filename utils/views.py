from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render


@login_required
def test_template(request):
    if request.user.is_superuser:
        return render(request, "email/invite.html")
    return Http404
