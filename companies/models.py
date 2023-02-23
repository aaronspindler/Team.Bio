from datetime import timedelta
from decimal import Decimal

import tldextract as tldextract
from django.conf import settings
from django.db import models
from django.utils import timezone

from billing.models import StripeCustomer


class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    trial_days = models.IntegerField(default=settings.DEFAULT_TRIAL_DAYS)
    test_company = models.BooleanField(default=False)

    name = models.TextField(unique=True)
    url = models.URLField(unique=True)
    url_root = models.CharField(max_length=250, unique=True)

    midpoint_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    midpoint_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        parsed = tldextract.extract(self.url)
        self.url_root = (parsed.domain + "." + parsed.suffix).lower()
        super().save(*args, **kwargs)

    def calculate_geo_midpoint(self):
        users = self.users.filter(is_active=True, lat__isnull=False, lng__isnull=False)
        lat_sum = Decimal(0.0)
        lng_sum = Decimal(0.0)
        if users.count() == 0:
            return 0.0, 0.0

        for user in users:
            lat_sum += Decimal(user.lat)
            lng_sum += Decimal(user.lng)

        self.midpoint_lat = lat_sum / users.count()
        self.midpoint_lng = lng_sum / users.count()
        self.save()

        return self.midpoint_lat, self.midpoint_lng

    @property
    def days_left_in_trial(self):
        return (self.created + timedelta(days=self.trial_days) - timezone.now()).days

    @property
    def in_trial_period(self):
        return self.days_left_in_trial > 0

    @property
    def is_billing_active(self):
        if self.get_billing_users:
            return True
        if self.in_trial_period:
            return True
        return False

    @property
    def get_owners(self):
        company_owners = self.owners.all()
        owners_list = []
        for company_owner in company_owners:
            owners_list.append(company_owner.owner)
        return owners_list

    @property
    def get_billing_users(self):
        users = StripeCustomer.objects.filter(user__in=self.get_owners)
        if users:
            return users.first()
        return None

    @property
    def get_active_users(self):
        return self.users.filter(is_active=True)

    @property
    def get_invited_users(self):
        return self.invites.all()

    class Meta:
        verbose_name_plural = "Companies"


class CompanyOwner(models.Model):
    company = models.ForeignKey(
        Company, related_name="owners", on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        "accounts.User", related_name="companies", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.company} {self.owner}"

    class Meta:
        unique_together = ("company", "owner")
        verbose_name = "Company Owner"
        verbose_name_plural = "Company Owners"


class Invite(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    company = models.ForeignKey(
        Company, related_name="invites", on_delete=models.CASCADE
    )
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.company} {self.email}"

    class Meta:
        unique_together = ("company", "email")
        verbose_name = "Invite"
        verbose_name_plural = "Invites"


class Team(models.Model):
    company = models.ForeignKey(Company, related_name="teams", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ("company", "name")
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class Location(models.Model):
    company = models.ForeignKey(
        Company, related_name="locations", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ("company", "name")
        verbose_name = "Location"
        verbose_name_plural = "Locations"
