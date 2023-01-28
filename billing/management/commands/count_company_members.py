from django.core.management.base import BaseCommand

from accounts.models import User
from billing.models import CompanyMemberCount
from companies.models import Company


class Command(BaseCommand):
    def handle(self, *args, **options):
        for company in Company.objects.all():
            num_users = User.objects.filter(company=company).count()
            CompanyMemberCount.objects.create(company=company, num_users=num_users)
            print(
                f"Created CompanyMemberCount for {company.name} with {num_users} user(s)"
            )
