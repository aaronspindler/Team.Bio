from django.db import models


class TriviaQuestion(models.Model):
    company = models.ForeignKey("companies.Company", related_name="trivia_questions", on_delete=models.CASCADE)
    question = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.question}"

    class Meta:
        verbose_name = "Trivia Question"
        verbose_name_plural = "Trivia Questions"


class TriviaQuestionOption(models.Model):
    question = models.ForeignKey(TriviaQuestion, related_name="trivia_answers", on_delete=models.CASCADE)
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
