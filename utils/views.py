from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from utils.social import get_social_image


@login_required
def test_template(request):
    if request.user.is_superuser:
        get_social_image(request.user.pk)
        return render(request, "_base.html")
    return Http404
