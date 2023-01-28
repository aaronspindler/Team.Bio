from django.shortcuts import redirect, render

from config import settings
from pages.utils import get_dog_image


def home(request):
    if request.user.is_authenticated and request.user.is_member_of_company:
        return redirect("company_home")
    return render(request, "pages/home.html")


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")


def terms_of_service(request):
    return render(request, "pages/terms_of_service.html")


def pricing(request):
    price = round(settings.PRICE_PER_USER / 100, 2)
    return render(request, "pages/pricing.html", {"price": price})


def billing_inactive(request):
    image = get_dog_image()
    return render(request, "pages/billing_inactive.html", {"image": image})
