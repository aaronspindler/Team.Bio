from decimal import Decimal

import googlemaps
from allauth.account.signals import user_signed_up
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from accounts.utils import (
    attempt_connect_user_to_a_company,
    attempt_connect_user_with_invites,
)
from utils.sms import create_admin_sms


class PetType(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Pet(models.Model):
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=400, blank=True, null=True)
    pet_type = models.ForeignKey(
        PetType, on_delete=models.CASCADE, blank=True, null=True
    )

    picture = models.ImageField(blank=True, null=True, upload_to="pets/")

    owner = models.ForeignKey(
        "accounts.User", related_name="pets", on_delete=models.CASCADE
    )

    @property
    def picture_url(self):
        if self.picture:
            return self.picture.url
        return "https://team-bio.s3.amazonaws.com/public/pets/dog-cat-transparent.jpg"

    def __str__(self):
        return self.name


class User(AbstractUser):
    company = models.ForeignKey(
        "companies.Company",
        related_name="users",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    email_prefix = models.CharField(max_length=250)
    email_root = models.CharField(max_length=250)

    # Profile
    profile_picture = models.ImageField(
        blank=True, null=True, upload_to="profile_picture/"
    )
    short_bio = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=240, blank=True, null=True)
    general_location = models.ForeignKey(
        "companies.Location", on_delete=models.CASCADE, blank=True, null=True
    )
    team = models.ForeignKey(
        "companies.Team", on_delete=models.CASCADE, blank=True, null=True
    )

    PERSONALITY_TYPE_CHOICES = (
        ("INTJ", "INTJ"),
        ("INTP", "INTP"),
        ("ENTJ", "ENTJ"),
        ("ENTP", "ENTP"),
        ("INFJ", "INFJ"),
        ("INFP", "INFP"),
        ("ENFJ", "ENFJ"),
        ("ENFP", "ENFP"),
        ("ISTJ", "ISTJ"),
        ("ISFJ", "ISFJ"),
        ("ESTJ", "ESTJ"),
        ("ESFJ", "ESFJ"),
        ("ISTP", "ISTP"),
        ("ISFP", "ISFP"),
        ("ESTP", "ESTP"),
        ("ESFP", "ESFP"),
    )
    personality_type = models.CharField(
        max_length=240, blank=True, null=True, choices=PERSONALITY_TYPE_CHOICES
    )

    CHINESE_ZODIAC_CHOICES = (
        ("Rat", "Rat"),
        ("Ox", "Ox"),
        ("Tiger", "Tiger"),
        ("Rabbit", "Rabbit"),
        ("Dragon", "Dragon"),
        ("Snake", "Snake"),
        ("Horse", "Horse"),
        ("Goat", "Goat"),
        ("Monkey", "Monkey"),
        ("Rooster", "Rooster"),
        ("Dog", "Dog"),
        ("Pig", "Pig"),
    )
    chinese_zodiac = models.CharField(
        max_length=240, blank=True, null=True, choices=CHINESE_ZODIAC_CHOICES
    )

    ZODIAC_SIGN_CHOICES = (
        ("Aries", "Aries"),
        ("Taurus", "Taurus"),
        ("Gemini", "Gemini"),
        ("Cancer", "Cancer"),
        ("Leo", "Leo"),
        ("Virgo", "Virgo"),
        ("Libra", "Libra"),
        ("Scorpio", "Scorpio"),
        ("Sagittarius", "Sagittarius"),
        ("Capricorn", "Capricorn"),
        ("Aquarius", "Aquarius"),
        ("Pisces", "Pisces"),
    )
    zodiac_sign = models.CharField(
        max_length=240, blank=True, null=True, choices=ZODIAC_SIGN_CHOICES
    )

    favourite_food = models.TextField(blank=True, null=True)
    favourite_movie = models.TextField(blank=True, null=True)
    favourite_travel_destination = models.TextField(blank=True, null=True)

    linkedin = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    github = models.CharField(max_length=200, blank=True, null=True)

    # Address Info
    place_id = models.TextField(blank=True, null=True)
    lat = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)

    address_1 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    prov_state = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    #   Non-User Editable
    start_date = models.DateField(blank=True, null=True)

    @property
    def profile_url(self):
        return reverse("user_profile", kwargs={"email_prefix": self.email_prefix})

    @property
    def profile_picture_url(self):
        url = "https://team-bio.s3.amazonaws.com/public/profile_picture/missing-profile-picture.jpg"
        if self.profile_picture:
            url = self.profile_picture.url
        return url

    class Meta:
        unique_together = ("company", "email_prefix")
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.company}/{self.email}"

    def save(self, *args, **kwargs):
        # Split up the email
        split_email = self.email.split("@")
        self.email_prefix = split_email[0].lower()
        self.email_root = split_email[1].lower()

        # Geocode the address
        self.lat, self.lng, self.place_id = self.geo_code_address()

        super().save(*args, **kwargs)

    @property
    def address_string(self):
        address = ""
        if self.address_1:
            address = self.address_1.strip()
        if self.city:
            address = f"{address} {self.city.strip()}"
        if self.prov_state:
            address = f"{address} {self.prov_state.strip()}"
        if self.country:
            address = f"{address} {self.country.strip()}"
        if self.postal_code:
            address = f"{address} {self.postal_code.strip()}"

        return address

    def geo_code_address(self):
        lat = None
        lng = None
        place_id = None

        # If there is no city or country, we can't geocode
        if not self.city or not self.country:
            return lat, lng, place_id

        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
        address = self.address_string
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            lat = Decimal(geocode_result[0]["geometry"]["location"]["lat"])
            lng = Decimal(geocode_result[0]["geometry"]["location"]["lng"])
            place_id = geocode_result[0]["place_id"]

        return lat, lng, place_id

    def personality_type_name(self):
        types = {
            "INTJ": "Architect",
            "INTP": "Logician",
            "ENTJ": "Commander",
            "ENTP": "Debater",
            "INFJ": "Advocate",
            "INFP": "Mediator",
            "ENFJ": "Protagonist",
            "ENFP": "Campaigner",
            "ISTJ": "Logistician",
            "ISFJ": "Defender",
            "ESTJ": "Executive",
            "ESFJ": "Consul",
            "ISTP": "Virtuoso",
            "ISFP": "Adventurer",
            "ESTP": "Entrepreneur",
            "ESFP": "Entertainer",
        }
        if self.personality_type:
            return types[self.personality_type]
        return ""

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_member_of_company(self):
        if self.company or self.companies.exists():
            return True
        return False

    # This is a signal receiver to try to connect a user to an existing company
    @receiver(user_signed_up)
    def allauth_user_signed_up(sender, request, user, **kwargs):
        create_admin_sms(f"TeamBio New User Signed Up: {user.email}")
        attempt_connect_user_with_invites(user)
        attempt_connect_user_to_a_company(user)
