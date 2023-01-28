import factory

from accounts.models import User
from companies.factories import CompanyFactory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    company = factory.SubFactory(CompanyFactory)
    short_bio = factory.Faker("text", max_nb_chars=240)
    title = factory.Faker("job")

    @factory.lazy_attribute
    def username(self):
        return f"{self.first_name}{self.last_name}"
