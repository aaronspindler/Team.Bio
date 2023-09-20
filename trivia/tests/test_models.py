from django.test import TestCase

from trivia.factories import (
    TriviaQuestionFactory,
    TriviaQuestionOptionFactory,
    TriviaUserAnswerFactory,
)


class TriviaUserAnswerTest(TestCase):
    def setUp(self):
        self.trivia_user_answer = TriviaUserAnswerFactory()

    def test_str_representation(self):
        self.assertEqual(str(self.trivia_user_answer), f"{self.trivia_user_answer.user} - {self.trivia_user_answer.question} - {self.trivia_user_answer.selected_option}")


class TriviaQuestionTest(TestCase):
    def setUp(self):
        self.trivia_question = TriviaQuestionFactory()

    def test_correct_answer(self):
        correct_option = TriviaQuestionOptionFactory(question=self.trivia_question, correct=True)
        self.assertEqual(self.trivia_question.correct_answer(), correct_option.text)
