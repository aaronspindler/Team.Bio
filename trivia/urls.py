from django.urls import path

from .views import answer_trivia_question, home, leaderboard

urlpatterns = [
    path("", home, name="trivia_home"),
    path("answer/<int:question>", answer_trivia_question, name="answer_trivia_question"),
    path("leaderboard", leaderboard, name="trivia_leaderboard"),
]
