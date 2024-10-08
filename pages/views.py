from django.shortcuts import get_object_or_404, redirect, render

from config import settings
from pages.models import BlogPost
from pages.utils import get_dog_image


def home(request):
    if request.user.is_authenticated and request.user.is_member_of_company:
        return redirect("company_home")
    return render(request, "pages/home.html")


def faq(request):
    price = round(settings.PRICE_PER_USER / 100, 2)
    default_trial_days = settings.DEFAULT_TRIAL_DAYS
    context = {
        "price": price,
        "default_trial_days": default_trial_days,
    }
    return render(request, "pages/faq.html", context)


def privacy_policy(request):
    return render(request, "pages/privacy_policy.html")


def terms_of_service(request):
    return render(request, "pages/terms_of_service.html")


def pricing(request):
    price = round(settings.PRICE_PER_USER / 100, 2)
    trial_days = settings.DEFAULT_TRIAL_DAYS
    return render(request, "pages/pricing.html", {"price": price, "trial_days": trial_days})


def billing_inactive(request):
    image = get_dog_image()
    return render(request, "pages/billing_inactive.html", {"image": image})


def blog(request):
    posts = BlogPost.objects.filter(published=True).select_related("posted_by").order_by("-created_at")
    return render(request, "pages/blog.html", {"posts": posts})


def blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, "pages/blog_post.html", {"post": post})
