from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render

from utils.tasks import create_admin_sms


@login_required
def test_code(request):
    if request.user.is_superuser:
        create_admin_sms.delay("Test code")
        return render(request, "_base.html")
    return Http404
