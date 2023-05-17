from django.urls import path

from .views import (
    billing_inactive,
    blog,
    blog_post,
    home,
    pricing,
    privacy_policy,
    terms_of_service,
)

urlpatterns = [
    path("", home, name="home"),
    path("blog", blog, name="blog"),
    path("blog/<slug:slug>", blog_post, name="blog_post"),
    path("privacy-policy", privacy_policy, name="privacy_policy"),
    path("terms-of-service", terms_of_service, name="terms_of_service"),
    path("pricing", pricing, name="pricing"),
    path("billing-inactive", billing_inactive, name="billing_inactive"),
]
