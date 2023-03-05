import factory

from companies.models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    url = factory.Faker("url")


class InviteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "companies.Invite"

    company = factory.SubFactory(CompanyFactory)
    email = factory.Faker("email")
