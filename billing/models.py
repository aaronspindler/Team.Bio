import stripe
from django.conf import settings
from django.db import models


class PromoCode(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    code = models.CharField(max_length=255, unique=True)
    num_free_days = models.IntegerField()

    def __str__(self):
        return self.code


class PaymentAttempt(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    customer = models.ForeignKey(
        "billing.StripeCustomer", on_delete=models.CASCADE, null=True, blank=True
    )
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE)
    amount = models.IntegerField()

    failed = models.BooleanField(default=False)
    failed_message = models.TextField(blank=True, null=True)


class CompanyMemberCount(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE)
    num_users = models.IntegerField()


class StripeCustomer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255)
    setup_intent_id = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

    def charge_customer(self, amount):
        """
        Charge the customer a certain amount
        amount: int - amount to charge in cents
        """
        payment_attempt = PaymentAttempt.objects.create(
            customer=self, company=self.user.company, amount=amount
        )
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                customer=self.stripe_customer_id,
                payment_method=self.payment_method,
                off_session=True,
                confirm=True,
            )
        except Exception as e:
            payment_attempt.failed = True
            payment_attempt.failed_message = str(e)
            payment_attempt.save()

    def invoice_customer(self, num_users):
        """
        Invoice the customer for a certain number of users
        num_users: int - number of users to invoice
        """
        payment_attempt = PaymentAttempt.objects.create(
            customer=self,
            company=self.user.company,
            amount=num_users * settings.PRICE_PER_USER,
        )
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            invoice = stripe.Invoice.create(
                customer=self.stripe_customer_id,
                auto_advance=True,
                collection_method="charge_automatically",
                default_payment_method=self.payment_method,
                currency="usd",
                automatic_tax={"enabled": True},
            )
            stripe.InvoiceItem.create(
                unit_amount=settings.PRICE_PER_USER,
                quantity=num_users,
                currency="usd",
                customer=self.stripe_customer_id,
                description="Per member, per month",
                invoice=invoice,
                tax_behavior="exclusive",
                tax_code="txcd_10103001",
            )
            stripe.Invoice.finalize_invoice(invoice, auto_advance=True)
        except Exception as e:
            payment_attempt.failed = True
            payment_attempt.failed_message = str(e)
            payment_attempt.save()
