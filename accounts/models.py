from allauth.account.signals import user_signed_up
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.dispatch import receiver

from companies.models import Company


class CustomUser(AbstractUser):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.email

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_member_of_company(self):
        if self.company or self.companies.exists():
            return True
        return False

    @property
    def email_root(self):
        return self.email.split('@')[1].lower()

    @receiver(user_signed_up)
    def attempt_connect_user_to_company_after_signup(sender, request, user, **kwargs):
        # Get user email root
        user_email_root = user.email_root
        # look for companies with url=email_root
        companies = Company.objects.filter(url_root=user_email_root)
        # if only 1 company found, proceed
        if companies.count() == 1:
            # set the users company to the found company
            user.company = companies.first()
            user.save()
        # if no company found, just continue
        elif companies.count() == 0:
            return
        # if multiple found throw an error
        else:
            raise Exception(f'Too many companies found with the same url_root: {user_email_root}')

