from django.test import TestCase

from trivia.factories import (
    TriviaQuestionFactory,
    TriviaQuestionOptionFactory,
    TriviaUserAnswerFactory,
)


class TriviaFactoriesTest(TestCase):
    def test_trivia_question_factory(self):
        trivia_question = TriviaQuestionFactory()
        self.assertIsNotNone(trivia_question.company)
        self.assertIsNotNone(trivia_question.question)

    def test_trivia_question_option_factory(self):
        trivia_question_option = TriviaQuestionOptionFactory()
        self.assertIsNotNone(trivia_question_option.question)
        self.assertIsNotNone(trivia_question_option.text)
        self.assertIsNotNone(trivia_question_option.correct)

    def test_trivia_user_answer_factory(self):
        trivia_user_answer = TriviaUserAnswerFactory()
        self.assertIsNotNone(trivia_user_answer.question)
        self.assertIsNotNone(trivia_user_answer.selected_option)
        self.assertIsNotNone(trivia_user_answer.user)
