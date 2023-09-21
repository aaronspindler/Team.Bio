import random

import factory

from companies.models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.LazyAttribute(lambda _: f"{factory.Faker('company')} {random.randint(1, 100)}")

    @factory.lazy_attribute
    def url(self):
        return f"https://{self.name.replace(' ', '').lower()}.com"


class InviteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "companies.Invite"

    company = factory.SubFactory(CompanyFactory)
    email = factory.Faker("email")
