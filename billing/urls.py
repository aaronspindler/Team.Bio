from django.urls import path

from . import views

urlpatterns = [
    path("success", views.success),
    path("cancel", views.cancel),
    path("config", views.stripe_config, name="stripe_config"),
    path("create-checkout-session", views.create_checkout_session),
    path("webhook", views.stripe_webhook),
]
