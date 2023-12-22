from django.urls import path

from .views import (
    answer_trivia_question,
    create_trivia_question,
    delete_trivia_question,
    edit_trivia_question,
    generate_question,
    home,
    leaderboard,
    management,
    publish_trivia_question,
)

urlpatterns = [
    path("", home, name="trivia_home"),
    path("<int:question>/answer", answer_trivia_question, name="answer_trivia_question"),
    path("<int:question>/edit/", edit_trivia_question, name="edit_trivia_question"),
    path("<int:question>/delete/", delete_trivia_question, name="delete_trivia_question"),
    path("<int:question>/publish/", publish_trivia_question, name="publish_trivia_question"),
    path("leaderboard", leaderboard, name="trivia_leaderboard"),
    path("management", management, name="trivia_management"),
    path("create", create_trivia_question, name="create_trivia_question"),
    path("generate", generate_question, name="generate_question"),
]
