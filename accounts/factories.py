import random

import factory

from accounts.models import Pet, PetType, User
from companies.factories import CompanyFactory

PERSONALITY_TYPE_CHOICES = [x[0] for x in User.PERSONALITY_TYPE_CHOICES]
CHINESE_ZODIAC_CHOICES = [x[0] for x in User.CHINESE_ZODIAC_CHOICES]
ZODIAC_CHOICES = [x[0] for x in User.ZODIAC_SIGN_CHOICES]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    company = factory.SubFactory(CompanyFactory)
    short_bio = factory.Faker("text", max_nb_chars=240)
    title = factory.Faker("job")
    is_active = True

    @factory.lazy_attribute
    def username(self):
        return f"{self.first_name}{self.last_name}"

    @factory.lazy_attribute
    def team(self):
        teams = list(self.company.teams.all())
        teams.append(None)
        return random.choice(teams)

    @factory.lazy_attribute
    def general_location(self):
        locations = list(self.company.locations.all())
        locations.append(None)
        return random.choice(locations)

    @factory.lazy_attribute
    def personality_type(self):
        return random.choice(PERSONALITY_TYPE_CHOICES)

    @factory.lazy_attribute
    def chinese_zodiac(self):
        return random.choice(CHINESE_ZODIAC_CHOICES)

    @factory.lazy_attribute
    def zodiac_sign(self):
        return random.choice(ZODIAC_CHOICES)

    @factory.lazy_attribute
    def linkedin(self):
        return f"{self.first_name}{self.last_name}"

    @factory.lazy_attribute
    def twitter(self):
        return f"{self.first_name}{self.last_name}"

    @factory.lazy_attribute
    def github(self):
        return f"{self.first_name}{self.last_name}"


class PetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pet

    name = factory.Faker("first_name")
    owner = factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def pet_type(self):
        return random.choice(list(PetType.objects.all()))
