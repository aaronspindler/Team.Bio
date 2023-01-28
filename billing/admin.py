from django.contrib import admin

from billing.models import PaymentAttempt, StripeCustomer

admin.site.register(StripeCustomer)
admin.site.register(PaymentAttempt)
