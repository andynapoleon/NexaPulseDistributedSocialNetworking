from django.urls import path
from . import views

urlpatterns = [
    path("test/", views.test, name="test"),
    # Add other URL patterns for handling likes, comments, etc.
]
