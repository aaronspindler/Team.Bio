from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Avg
from django.utils import timezone

from billing.models import CompanyMemberCount, PaymentAttempt
from companies.models import Company


class Command(BaseCommand):
    def handle(self, *args, **options):
        for company in Company.objects.all():
            print(f"{company} (PK: {company.pk})")
            if company.in_trial_period:
                print("\t In trial period")
            else:
                # Calculate the average number of users the company had in the last 30 days
                average_num_users = int(
                    CompanyMemberCount.objects.filter(
                        company=company, created__gt=timezone.now() - timedelta(days=30)
                    ).aggregate(Avg("num_users"))["num_users__avg"]
                )
                print(f"\t Average of {average_num_users} users in the last 30 days")
                print(f"\t Current number of users: {company.get_active_users.count()}")

                amount_to_bill_int = average_num_users * settings.PRICE_PER_USER
                print(
                    f"\t Amount to bill: ${round(Decimal(amount_to_bill_int / 100), 2)}"
                )

                billing_user = company.get_billing_user
                if not billing_user:
                    print("\t Has no billing user")
                    # Create a failed payment attempt
                    PaymentAttempt.objects.create(
                        company=company,
                        amount=amount_to_bill_int,
                        failed=True,
                        failed_message="No billing user",
                    )
                else:
                    print(f"\t Billing user: {billing_user} (PK: {billing_user.pk})")
                    # Invoice the customer
                    if company.test_company:
                        print("\t Test company, not invoicing")
                    else:
                        billing_user.invoice_customer(average_num_users)
                        print(f"\t Invoiced customer for {average_num_users} users")
