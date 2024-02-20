from django.urls import path

from . import views # . referes to the current module we are in

from django.urls import path

from . import views

urlpatterns = [
    # ex: /users/5/
    path("<int:author_id>/", views.detail, name="detail"),
    # ex: /users/5/results/
    path("<int:author_id>/results/", views.results, name="results"),
    # ex: /users/5/vote/
    path("<int:author_id>/vote/", views.vote, name="vote"),
]