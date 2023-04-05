from django.contrib import admin

from billing.models import PaymentAttempt, PromoCode, StripeCustomer

admin.site.register(StripeCustomer)
admin.site.register(PaymentAttempt)
admin.site.register(PromoCode)
