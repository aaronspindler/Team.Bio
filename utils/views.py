from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render


@login_required
def test_code(request):
    if request.user.is_superuser:
        messages.success(request, "SUCCESS")
        messages.error(request, "ERROR")
        messages.info(request, "INFO")
        messages.warning(request, "WARNING")
        return render(request, "_base.html")
    return Http404
