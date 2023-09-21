from django.contrib import admin

from trivia.models import TriviaQuestion, TriviaQuestionOption, TriviaUserAnswer


@admin.register(TriviaQuestion)
class TriviaQuestionAdmin(admin.ModelAdmin):
    list_display = ["company", "question", "published"]
    list_filter = ["company", "published"]
    model = TriviaQuestion

    actions = ["publish"]

    @admin.action(description="Publish trivia question(s)")
    def publish(self, request, queryset):
        queryset.update(published=True)


@admin.register(TriviaQuestionOption)
class TriviaQuestionOptionAdmin(admin.ModelAdmin):
    list_display = ["question", "text", "correct"]
    list_filter = ["question", "question__company"]
    model = TriviaQuestionOption


@admin.register(TriviaUserAnswer)
class TriviaUserAnswerAdmin(admin.ModelAdmin):
    list_display = ["user", "question", "selected_option"]
    list_filter = ["question", "question__company"]
    model = TriviaUserAnswer
