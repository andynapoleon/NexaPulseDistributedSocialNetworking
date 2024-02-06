from django.urls import path

from . import views # . referes to the current module we are in

urlpatterns = [
    path("", views.index, name="index"),
]