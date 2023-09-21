import factory

from accounts.factories import UserFactory
from companies.factories import CompanyFactory
from trivia.models import TriviaQuestion, TriviaQuestionOption, TriviaUserAnswer


class TriviaQuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TriviaQuestion

    company = factory.SubFactory(CompanyFactory)
    question = factory.Faker("paragraph", nb_sentences=1)
    published = True


class TriviaQuestionOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TriviaQuestionOption

    question = factory.SubFactory(TriviaQuestionFactory)
    text = factory.Faker("sentence")
    correct = factory.Faker("boolean")


class TriviaUserAnswerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TriviaUserAnswer

    question = factory.SubFactory(TriviaQuestionFactory)
    selected_option = factory.SubFactory(TriviaQuestionOptionFactory)
    user = factory.SubFactory(UserFactory)
