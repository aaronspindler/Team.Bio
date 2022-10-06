from allauth.account.signals import user_signed_up
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.dispatch import receiver

from accounts.utils import attempt_connect_user_to_a_company
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
    def allauth_user_signed_up(sender, request, user, **kwargs):
        attempt_connect_user_to_a_company(user)
