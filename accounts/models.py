from django.contrib.auth.models import AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.email
