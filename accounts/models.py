from allauth.account.signals import user_signed_up
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.dispatch import receiver

from accounts.utils import attempt_connect_user_to_a_company


class CustomUser(AbstractUser):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, blank=True, null=True)
    email_prefix = models.CharField(max_length=250)
    email_root = models.CharField(max_length=250)

    # Profile
    profile_picture = models.ImageField(null=True, upload_to='profile_picture/')
    short_bio = models.CharField(max_length=240, blank=True, null=True)

    class Meta:
        unique_together = ("company", "email_prefix")

    def __str__(self):
        return f'{self.company}/{self.email}'

    def save(self, *args, **kwargs):
        # Split up the email
        split_email = self.email.split('@')
        self.email_prefix = split_email[0].lower()
        self.email_root = split_email[1].lower()

        super().save(*args, **kwargs)

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_member_of_company(self):
        if self.company or self.companies.exists():
            return True
        return False

    @receiver(user_signed_up)
    def allauth_user_signed_up(sender, request, user, **kwargs):
        attempt_connect_user_to_a_company(user)
