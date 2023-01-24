from django.contrib import admin

from billing.models import StripeCustomer

admin.site.register(StripeCustomer)
