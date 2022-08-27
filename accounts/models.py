from django.contrib.auth.models import AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.email

    @property
    def is_member_of_company(self):
        if self.company or self.companies.exists():
            return True
        return False
