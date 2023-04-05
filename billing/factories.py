import factory

from companies.models import PromoCode


class PromoCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PromoCode

    code = "test"
    num_free_days = 365
