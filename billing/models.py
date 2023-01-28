import stripe
from django.conf import settings
from django.db import models


class StripeCustomer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    setupIntentId = models.CharField(max_length=255)
    paymentMethod = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

    def charge_customer(self, amount):
        """
        Charge the customer a certain amount
        amount: int - amount to charge in cents
        """
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.create(
            amount=amount,
            currency="usd",
            customer=self.stripeCustomerId,
            payment_method=self.paymentMethod,
            off_session=True,
            confirm=True,
        )

    def invoice_customer(self, num_users):
        """
        Invoice the customer for a certain number of users
        num_users: int - number of users to invoice
        """
        stripe.api_key = settings.STRIPE_SECRET_KEY
        invoice = stripe.Invoice.create(
            customer=self.stripeCustomerId,
            auto_advance=True,
            collection_method="charge_automatically",
            default_payment_method=self.paymentMethod,
            automatic_tax={"enabled": True},
        )
        stripe.InvoiceItem.create(
            unit_amount=settings.PRICE_PER_USER,
            quantity=num_users,
            currency="usd",
            customer=self.stripeCustomerId,
            description="Per member, per month",
            invoice=invoice,
            tax_behavior="exclusive",
            tax_code="txcd_10103001",
        )
        stripe.Invoice.finalize_invoice(invoice, auto_advance=True)
