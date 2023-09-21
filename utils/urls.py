from django.urls import path

from utils.views import test_code

urlpatterns = [
    path("test-code", test_code, name="test-code"),
]
