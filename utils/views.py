from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render


@login_required
def test_template(request):
    if request.user.is_superuser:
        mid_lat, mid_lng = (
            request.user.company.midpoint_lat,
            request.user.company.midpoint_lng,
        )
        user_points = (
            request.user.company.users.filter(
                is_active=True, lat__isnull=False, lng__isnull=False
            )
            .select_related("team__name")
            .values("lng", "lat", "team__name")
        )
        cleaned_user_points = []
        for user in user_points:
            cleaned_user_points.append(
                [
                    user["lng"],
                    user["lat"],
                    user["team__name"] if user["team__name"] else "No Team",
                ]
            )
        data = {
            "mid_lng": mid_lng,
            "mid_lat": mid_lat,
            "user_points": cleaned_user_points,
            "api_key": settings.MAPBOX_API_KEY,
        }
        print(data)
        return render(request, "companies/map.html", data)
    return Http404
