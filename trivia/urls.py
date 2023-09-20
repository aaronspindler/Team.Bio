from django.urls import path

from .views import trivia

urlpatterns = [
    path("", trivia, name="trivia_home"),
]
