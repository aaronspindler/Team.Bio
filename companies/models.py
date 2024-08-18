from datetime import timedelta
from decimal import Decimal

import tldextract as tldextract
from colorfield.fields import ColorField
from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.utils import timezone

from billing.models import PromoCode, StripeCustomer
from config.storage_backends import PrivateStorage


class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    trial_days = models.IntegerField(default=settings.DEFAULT_TRIAL_DAYS)
    test_company = models.BooleanField(default=False, help_text="Used for develop testing companies")
    billing_disabled = models.BooleanField(default=False, help_text="Used for companies where we do not want to bill them")

    name = models.TextField(unique=True)
    url = models.URLField(unique=True)
    url_root = models.CharField(max_length=250, unique=True)

    # Company Features
    map_enabled = models.BooleanField(default=True)
    links_enabled = models.BooleanField(default=True)
    trivia_enabled = models.BooleanField(default=True)

    # Map Stuff
    midpoint_lat = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    midpoint_lng = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    max_lat = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    min_lat = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    max_lng = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    min_lng = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        parsed = tldextract.extract(self.url)
        self.url_root = (parsed.domain + "." + parsed.suffix).lower()
        super().save(*args, **kwargs)

    def has_recently_generated_trivia_question(self):
        recent_trivia_questions = self.trivia_generation_requests.filter(completed=True, created__gte=timezone.now() - timedelta(minutes=5))
        return recent_trivia_questions.count() >= 3

    def should_show_map(self):
        return self.users.filter(is_active=True, lat__isnull=False, lng__isnull=False).exists() and self.map_enabled

    def calculate_geo_midpoint(self):
        users = self.users.filter(is_active=True, lat__isnull=False, lng__isnull=False)
        if not users.exists():
            return 0.0, 0.0

        avg_values = users.aggregate(avg_lat=Avg("lat"), avg_lng=Avg("lng"))
        self.midpoint_lat = avg_values["avg_lat"]
        self.midpoint_lng = avg_values["avg_lng"]
        self.save(update_fields=["midpoint_lat", "midpoint_lng"])

        return self.midpoint_lat, self.midpoint_lng

    def calculate_map_bounds(self):
        users = self.users.filter(is_active=True, lat__isnull=False, lng__isnull=False)
        if not users.exists():
            return ([0, 0], [0, 0])

        aggregates = users.aggregate(min_lat=models.Min("lat"), max_lat=models.Max("lat"), min_lng=models.Min("lng"), max_lng=models.Max("lng"))

        padding = Decimal("0.25")
        for key, value in aggregates.items():
            setattr(self, key, Decimal(value).quantize(Decimal("0.001")) + (-padding if "min" in key else padding))

        self.save(update_fields=["min_lat", "max_lat", "min_lng", "max_lng"])

        return ([self.min_lng, self.min_lat], [self.max_lng, self.max_lat])

    def get_map_sw_corner(self):
        return f"[{self.min_lng}, {self.min_lat}]"

    def get_map_ne_corner(self):
        return f"[{self.max_lng}, {self.max_lat}]"

    def get_map_data(self):
        if not self.should_show_map():
            return {"show_map": False}

        teams = list(self.teams.all()) + [None]  # Include "No Team"
        map_teams = []

        for team in teams:
            team_name = team.name if team else "No Team"
            team_color = team.color.lower() if team else "#000000"

            user_points = self.users.filter(is_active=True, lat__isnull=False, lng__isnull=False, team=team).values("lng", "lat", "first_name", "last_name", "city", "prov_state")

            cleaned_user_points = [
                [
                    float(user["lng"]),
                    float(user["lat"]),
                    f"{user['first_name']} {user['last_name']}<br>{user['city']}, {user['prov_state']}<br>{team_name}",
                ]
                for user in user_points
            ]

            map_teams.append((team_name, team_color, cleaned_user_points))

        return {
            "mid_lng": self.midpoint_lng,
            "mid_lat": self.midpoint_lat,
            "sw_corner": self.get_map_sw_corner(),
            "ne_corner": self.get_map_ne_corner(),
            "map_teams": map_teams,
            "api_key": settings.MAPBOX_API_KEY,
            "show_map": True,
        }

    def get_link_data(self):
        if not self.links_enabled:
            return {"show_links": False}

        links = self.links.values("name", "url")
        data = {
            "links": links,
            "show_links": True,
        }
        return data

    @property
    def days_left_in_trial(self):
        return (self.created + timedelta(days=self.trial_days) - timezone.now()).days

    @property
    def in_trial_period(self):
        return self.days_left_in_trial > 0

    @property
    def is_enabled(self):
        if self.get_billing_user:
            return True
        if self.in_trial_period:
            return True
        if self.test_company:
            return True
        if self.billing_disabled:
            return True
        return False

    @property
    def get_owners(self):
        return list(CompanyOwner.objects.filter(company=self).values_list("owner", flat=True))

    @property
    def get_billing_user(self):
        users = StripeCustomer.objects.filter(user__pk__in=self.get_owners)
        if users:
            return users.first()
        return None

    @property
    def get_active_users(self):
        return self.users.filter(is_active=True).order_by("first_name", "last_name")

    @property
    def get_invited_users(self):
        return self.invites.all()

    class Meta:
        verbose_name_plural = "Companies"


class CompanyOwner(models.Model):
    company = models.ForeignKey(Company, related_name="owners", on_delete=models.CASCADE)
    owner = models.ForeignKey("accounts.User", related_name="companies", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.company} {self.owner}"

    class Meta:
        unique_together = ("company", "owner")
        verbose_name = "Company Owner"
        verbose_name_plural = "Company Owners"


class BulkInviteRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    processed = models.BooleanField(default=False)

    company = models.ForeignKey(Company, related_name="bulk_invite_requests", on_delete=models.CASCADE)
    file = models.FileField(upload_to="bulk_invite_requests/", storage=PrivateStorage())
    requested_by = models.ForeignKey("accounts.User", related_name="bulk_invite_requests", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.company} {self.file}"

    class Meta:
        verbose_name = "Bulk Invite Request"
        verbose_name_plural = "Bulk Invite Requests"


class Invite(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    company = models.ForeignKey(Company, related_name="invites", on_delete=models.CASCADE)
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
    color = ColorField(default="#FF0000")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ("company", "name")
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class Location(models.Model):
    company = models.ForeignKey(Company, related_name="locations", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ("company", "name")
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class Link(models.Model):
    company = models.ForeignKey(Company, related_name="links", on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    url = models.CharField(max_length=500)

    def save(self, *args, **kwargs):
        if not self.url.startswith("http"):
            self.url = f"http://{self.url}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        unique_together = ("company", "name")
        verbose_name = "Link"
        verbose_name_plural = "Links"
