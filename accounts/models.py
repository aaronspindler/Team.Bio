from allauth.account.signals import user_signed_up
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver

from accounts.utils import attempt_connect_user_to_a_company


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
    short_bio = models.CharField(max_length=240, blank=True, null=True)
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
    lat = models.TextField(blank=True, null=True)
    lon = models.TextField(blank=True, null=True)
    address_1 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    prov_state = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)

    #   Non-User Editable
    start_date = models.DateField(blank=True, null=True)

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

        super().save(*args, **kwargs)

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
        attempt_connect_user_to_a_company(user)
