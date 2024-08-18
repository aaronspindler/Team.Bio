from django.test import TestCase
from django.urls import reverse

from accounts.factories import UserFactory
from trivia.factories import (
    TriviaQuestionFactory,
    TriviaQuestionOptionFactory,
    TriviaUserAnswerFactory,
)
from trivia.models import TriviaQuestion, TriviaUserAnswer


class TriviaViewTests(TestCase):
    def setUp(self):
        self.trivia_question = TriviaQuestionFactory()
        self.company = self.trivia_question.company
        self.user = UserFactory(company=self.company)
        self.client.force_login(user=self.user)

    def test_home_trivia_disabled_redirect(self):
        self.company.trivia_enabled = False
        self.company.save()
        response = self.client.get(reverse("trivia_home"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "companies/home.html")
        self.assertNotContains(response, "Trivia")

    def test_home_trivia_enabled(self):
        self.company.trivia_enabled = True
        self.company.save()
        response = self.client.get(reverse("trivia_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trivia/home.html")
        self.assertContains(response, "Trivia")

    def test_trivia_home_empty_state(self):
        TriviaQuestion.objects.all().delete()
        response = self.client.get(reverse("trivia_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trivia/home.html")
        self.assertContains(response, "No trivia questions")

    def test_trivia_home_dont_show_other_co_trivia_questions(self):
        other_co_question = TriviaQuestionFactory()
        self.assertNotEqual(self.company, other_co_question.company)
        response = self.client.get(reverse("trivia_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "trivia/home.html")
        self.assertNotContains(response, other_co_question.question)
        self.assertContains(response, self.trivia_question.question)

    def test_answer_trivia_question_does_not_exist(self):
        response = self.client.post(reverse("answer_trivia_question", args=[1000]))
        self.assertEqual(response.status_code, 404)

    def test_answer_trivia_question_get(self):
        response = self.client.get(reverse("answer_trivia_question", args=[self.trivia_question.pk]))
        self.assertEqual(response.status_code, 405)

    def test_answer_trivia_question_already_answered(self):
        TriviaUserAnswerFactory(user=self.user, question=self.trivia_question)
        response = self.client.post(reverse("answer_trivia_question", args=[self.trivia_question.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("trivia_home"))

    def test_answer_trivia_question_correctly(self):
        correct_option = TriviaQuestionOptionFactory(question=self.trivia_question, correct=True)
        data = {str(self.trivia_question.pk): correct_option.text}
        self.assertFalse(TriviaUserAnswer.objects.filter(user=self.user, question=self.trivia_question).exists())
        response = self.client.post(reverse("answer_trivia_question", args=[self.trivia_question.pk]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("trivia_home"))
        self.assertTrue(TriviaUserAnswer.objects.filter(user=self.user, question=self.trivia_question).exists())
