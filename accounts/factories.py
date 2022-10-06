import factory

from accounts.models import CustomUser
from companies.factories import CompanyFactory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    company = factory.SubFactory(CompanyFactory)
    short_bio = factory.Faker('text', max_nb_chars=240)

    @factory.lazy_attribute
    def username(self):
        return f'{self.first_name}{self.last_name}'
