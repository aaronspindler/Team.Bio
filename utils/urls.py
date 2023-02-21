from django.urls import path

from utils.views import test_template

urlpatterns = [
    path("test-template", test_template, name="test-template"),
]
