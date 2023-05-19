import random

import faker
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.factories import PetFactory, UserFactory
from accounts.models import PetType
from companies.models import Company, Location, Team
from utils.images import get_image_from_url

fake = faker.Faker()

UNSPLASH_ACCESS_KEY = settings.UNSPLASH_ACCESS_KEY


class Command(BaseCommand):
    def get_image_file(self, query):
        url = f"https://api.unsplash.com/photos/random?client_id={UNSPLASH_ACCESS_KEY}&query={query}&orientation=portrait"
        response = requests.get(url)
        if response.status_code == 200:
            json = response.json()
            image_url = json["urls"]["regular"]
            return get_image_from_url(image_url)
        return None

    def get_profile_image(self):
        file = self.get_image_file("headshot")
        return file

    def make_pets(self, user):
        options = ["Dog", "Cat"]
        num_pets = random.randint(0, 3)
        for _ in range(num_pets):
            animal_type = random.choice(options)
            file = self.get_image_file(animal_type)
            pet_type = PetType.objects.get(name=animal_type)
            pet = PetFactory(owner=user, pet_type=pet_type)
            pet.picture.save(f"fake_{pet.name}.jpg", file, save=True)
            pet.save()

    def get_address(self):
        """
        Gets a real address by scraping this website
        """
        urls = [
            "https://www.bestrandoms.com/random-address-in-ca?quantity=1",
            "https://www.bestrandoms.com/random-address-in-us?quantity=1",
        ]
        response = requests.get(random.choice(urls))
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.find("div", {"class": "content"})
        data_list = content.find("ul", {"class": "list-unstyled"})
        li = data_list.find("li")
        spans = li.find_all("span")
        address = {}
        for span in spans:
            header = span.find("b")
            value = span.text.replace(header.text, "").strip()
            if header.text == "Street:":
                address["address_1"] = value
            elif header.text == "City:":
                address["city"] = value
            elif header.text == "State/province/area: ":
                address["prov_state"] = value
            elif header.text == "Zip code":
                address["postal_code"] = value
            elif header.text == "Country":
                address["country"] = value
        return address

    def handle(self, *args, **options):
        num_people = 10
        company = Company.objects.get(pk=2)

        teams = [
            "Accounting",
            "Administration",
            "Business Development",
            "Customer Service",
            "Engineering",
            "Finance",
            "Human Resources",
            "Information Technology",
            "Legal",
            "Marketing",
            "Operations",
            "Product Management",
        ]
        for team_name in teams:
            team, created = Team.objects.get_or_create(name=team_name, company=company)
            if created:
                team.color = fake.unique.hex_color()
                team.save()

        with transaction.atomic():
            for _ in range(num_people):
                address = self.get_address()
                location = address["prov_state"]
                location, _ = Location.objects.get_or_create(
                    name=location, company=company
                )
                user = UserFactory(
                    company=company, general_location=location, **address
                )
                user.email = (
                    f"{user.first_name.lower()}.{user.last_name.lower()}@spindlers.ca"
                )
                print(user.email)
                user.title = user.title.title()
                file = self.get_profile_image()
                user.profile_picture.save(f"fake_{user.last_name}.jpg", file, save=True)
                user.save()
                self.make_pets(user)

            company.calculate_geo_midpoint()
            company.calculate_map_bounds()
