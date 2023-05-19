from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render


@login_required
def test_template(request):
    if request.user.is_superuser:
        request.user.set_social_profile_picture()
        return render(request, "_base.html")
    return Http404
