from django.urls import path

from .views import (
    answer_trivia_question,
    delete_trivia_question,
    home,
    leaderboard,
    management,
)

urlpatterns = [
    path("", home, name="trivia_home"),
    path("<int:question>/answer", answer_trivia_question, name="answer_trivia_question"),
    path("<int:question>/delete/", delete_trivia_question, name="delete_trivia_question"),
    path("leaderboard", leaderboard, name="trivia_leaderboard"),
    path("management", management, name="trivia_management"),
]
