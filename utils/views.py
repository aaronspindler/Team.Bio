from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render


@login_required
def test_template(request):
    if request.user.is_superuser:
        data = request.user.company.get_map_data()
        return render(request, "companies/map.html", data)
    return Http404
