from django.db import models


class TriviaQuestion(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    company = models.ForeignKey("companies.Company", related_name="trivia_questions", on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question}"

    def number_of_answers(self):
        return self.user_answers.count()

    def number_of_correct_answers(self):
        return self.user_answers.filter(selected_option__correct=True).count()

    def percentage_of_correct_answers(self):
        num_correct = self.number_of_correct_answers()
        num_answers = self.number_of_answers()
        if num_answers == 0:
            return 0
        return round(num_correct / num_answers * 100, 2)

    def correct_answer(self):
        return self.question_option.get(correct=True).text

    class Meta:
        verbose_name = "Trivia Question"
        verbose_name_plural = "Trivia Questions"


class TriviaQuestionOption(models.Model):
    question = models.ForeignKey(TriviaQuestion, related_name="question_option", on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question} - {self.text}"

    class Meta:
        verbose_name = "Trivia Question Option"
        verbose_name_plural = "Trivia Question Options"


class TriviaUserAnswer(models.Model):
    user = models.ForeignKey("accounts.User", related_name="trivia_answers", on_delete=models.CASCADE)
    question = models.ForeignKey(TriviaQuestion, related_name="user_answers", on_delete=models.CASCADE)
    selected_option = models.ForeignKey(TriviaQuestionOption, related_name="user_answers", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.question} - {self.selected_option}"

    class Meta:
        unique_together = ("user", "question")
        verbose_name = "Trivia User Answer"
        verbose_name_plural = "Trivia User Answers"
