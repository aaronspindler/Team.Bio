from django.db import IntegrityError
from django.test import TestCase

from trivia.factories import (
    TriviaQuestionFactory,
    TriviaQuestionOptionFactory,
    TriviaUserAnswerFactory,
)


class TriviaUserAnswerTest(TestCase):
    def setUp(self):
        self.trivia_user_answer = TriviaUserAnswerFactory()

    def test_no_duplicate_answers_from_same_user(self):
        with self.assertRaises(IntegrityError):
            TriviaUserAnswerFactory(user=self.trivia_user_answer.user, question=self.trivia_user_answer.question)


class TriviaQuestionTest(TestCase):
    def setUp(self):
        self.trivia_question = TriviaQuestionFactory()

    def test_correct_answer(self):
        correct_option = TriviaQuestionOptionFactory(question=self.trivia_question, correct=True)
        incorrect_option = TriviaQuestionOptionFactory(question=self.trivia_question, correct=False)
        self.assertEqual(self.trivia_question.correct_answer(), correct_option.text)
        self.assertNotEqual(self.trivia_question.correct_answer(), incorrect_option.text)

    def test_number_of_answers(self):
        for _ in range(5):
            TriviaUserAnswerFactory(question=self.trivia_question)
        self.assertEqual(self.trivia_question.number_of_answers(), 5)

    def test_number_of_correct_answers(self):
        correct_option = TriviaQuestionOptionFactory(question=self.trivia_question, correct=True)
        incorrect_option = TriviaQuestionOptionFactory(question=self.trivia_question, correct=False)
        TriviaUserAnswerFactory(question=self.trivia_question, selected_option=correct_option)
        TriviaUserAnswerFactory(question=self.trivia_question, selected_option=correct_option)
        TriviaUserAnswerFactory(question=self.trivia_question, selected_option=incorrect_option)
        self.assertEqual(self.trivia_question.number_of_correct_answers(), 2)

    def test_perceentage_of_correct_answers(self):
        correct_option = TriviaQuestionOptionFactory(question=self.trivia_question, correct=True)
        incorrect_option = TriviaQuestionOptionFactory(question=self.trivia_question, correct=False)
        TriviaUserAnswerFactory(question=self.trivia_question, selected_option=correct_option)
        TriviaUserAnswerFactory(question=self.trivia_question, selected_option=correct_option)
        TriviaUserAnswerFactory(question=self.trivia_question, selected_option=incorrect_option)
        self.assertEqual(self.trivia_question.percentage_of_correct_answers(), 66.67)
