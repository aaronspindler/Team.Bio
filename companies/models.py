from datetime import timedelta
from decimal import Decimal

import tldextract as tldextract
from colorfield.fields import ColorField
from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.utils import timezone

from billing.models import PromoCode, StripeCustomer


class Company(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    promo_code = models.ForeignKey(
        PromoCode, on_delete=models.SET_NULL, null=True, blank=True
    )
    trial_days = models.IntegerField(default=settings.DEFAULT_TRIAL_DAYS)
    test_company = models.BooleanField(
        default=False, help_text="Used for develop testing companies"
    )
    billing_disabled = models.BooleanField(
        default=False, help_text="Used for companies where we do not want to bill them"
    )

    name = models.TextField(unique=True)
    url = models.URLField(unique=True)
    url_root = models.CharField(max_length=250, unique=True)

    # Company Features
    map_enabled = models.BooleanField(default=True)
    links_enabled = models.BooleanField(default=True)

    # Map Stuff
    midpoint_lat = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True
    )
    midpoint_lng = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True
    )
    max_lat = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True
    )
    min_lat = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True
    )
    max_lng = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True
    )
    min_lng = models.DecimalField(
        max_digits=12, decimal_places=6, null=True, blank=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        parsed = tldextract.extract(self.url)
        self.url_root = (parsed.domain + "." + parsed.suffix).lower()
        super().save(*args, **kwargs)

    def should_show_map(self):
        return (
            self.users.filter(
                is_active=True, lat__isnull=False, lng__isnull=False
            ).exists()
            and self.map_enabled
        )

    def calculate_geo_midpoint(self):
        users = self.users.filter(is_active=True, lat__isnull=False, lng__isnull=False)
        if users.count() == 0:
            return 0.0, 0.0

        self.midpoint_lat = users.aggregate(Avg("lat"))["lat__avg"]
        self.midpoint_lng = users.aggregate(Avg("lng"))["lng__avg"]
        self.save()

        return self.midpoint_lat, self.midpoint_lng

    def calculate_map_bounds(self):
        users = self.users.filter(is_active=True, lat__isnull=False, lng__isnull=False)
        min_lat = Decimal(1000)
        max_lat = Decimal(-1000)
        min_lng = Decimal(1000)
        max_lng = Decimal(-1000)

        for user in users:
            lng = Decimal(user.lng)
            lat = Decimal(user.lat)
            if lat < min_lat:
                min_lat = lat
            if lat > max_lat:
                max_lat = lat
            if lng < min_lng:
                min_lng = lng
            if lng > max_lng:
                max_lng = lng

        padding = Decimal("0.25")
        self.min_lat = min_lat.quantize(Decimal("0.001")) - padding
        self.max_lat = max_lat.quantize(Decimal("0.001")) + padding
        self.min_lng = min_lng.quantize(Decimal("0.001")) - padding
        self.max_lng = max_lng.quantize(Decimal("0.001")) + padding
        self.save()

        return ([min_lng, min_lat], [max_lng, max_lat])

    def get_map_sw_corner(self):
        lng = str(self.min_lng)
        lat = str(self.min_lat)
        return f"[{lng}, {lat}]"

    def get_map_ne_corner(self):
        lng = str(self.max_lng)
        lat = str(self.max_lat)
        return f"[{lng}, {lat}]"

    def get_map_data(self):
        if not self.should_show_map():
            return {"show_map": False}

        mid_lat, mid_lng = (
            self.midpoint_lat,
            self.midpoint_lng,
        )

        teams = list(self.teams.all())
        teams.append(None)  # This is here so that we can have a "No Team" group
        map_teams = []
        for team in teams:
            team_name = "No Team"
            team_color = "#000000"
            if team:
                team_name = team.name
                team_color = team.color.lower()
            user_points = self.users.filter(
                is_active=True, lat__isnull=False, lng__isnull=False, team=team
            ).values("lng", "lat", "first_name", "last_name", "city", "prov_state")
            cleaned_user_points = []
            for user in user_points:
                lng = float(user["lng"])
                lat = float(user["lat"])

                cleaned_user_points.append(
                    [
                        lng,
                        lat,
                        f"{user.get('first_name')} {user.get('last_name')}<br>{user.get('city')}, {user.get('prov_state')}<br>{team_name}",
                    ]
                )
            map_teams.append((team_name, team_color, cleaned_user_points))

        data = {
            "mid_lng": mid_lng,
            "mid_lat": mid_lat,
            "sw_corner": self.get_map_sw_corner(),
            "ne_corner": self.get_map_ne_corner(),
            "map_teams": map_teams,
            "api_key": settings.MAPBOX_API_KEY,
            "show_map": True,
        }
        return data

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
        return list(
            CompanyOwner.objects.filter(company=self).values_list("owner", flat=True)
        )

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
    color = ColorField(default="#FF0000")

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


class TriviaQuestion(models.Model):
    company = models.ForeignKey(
        Company, related_name="trivia_questions", on_delete=models.CASCADE
    )
    question = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.question}"

    class Meta:
        verbose_name = "Trivia Question"
        verbose_name_plural = "Trivia Questions"


class TriviaQuestionOption(models.Model):
    question = models.ForeignKey(
        TriviaQuestion, related_name="trivia_answers", on_delete=models.CASCADE
    )
    text = models.CharField(max_length=500)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question} - {self.text}"

    class Meta:
        verbose_name = "Trivia Question Option"
        verbose_name_plural = "Trivia Question Options"


class TriviaUserAnswer(models.Model):
    user = models.ForeignKey(
        "accounts.User", related_name="trivia_answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        TriviaQuestion, related_name="user_answers", on_delete=models.CASCADE
    )
    selected_option = models.ForeignKey(
        TriviaQuestionOption, related_name="user_answers", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} - {self.question} - {self.selected_option}"

    class Meta:
        unique_together = ("user", "question")
        verbose_name = "Trivia User Answer"
        verbose_name_plural = "Trivia User Answers"
