from django.urls import path

from . import views # . referes to the current module we are in

urlpatterns = [
    # # ex: /users/5/
    # path("<int:user_id>/", views.detail, name="detail"),
    # # ex: /users/5/results/
    # path("<int:user_id>/results/", views.results, name="results"),
    # # ex: /users/5/vote/
    # path("<int:user_id>/vote/", views.vote, name="vote"),
]