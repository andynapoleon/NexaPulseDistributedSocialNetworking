from django.urls import path

from . import views  # . referes to the current module we are in

urlpatterns = [
    path("authors", views.AuthorList.as_view(), name="Author List"),
    path("authors/", views.AuthorList.as_view(), name="Author List"),
    path("authors/new/", views.AuthorCreate.as_view(), name="New author"),
    path("authors/remote/", views.AuthorRemote.as_view(), name="New remote author"),
    path(
        "authors/<str:author_id>/",
        views.AuthorDetail.as_view(),
        name="Get specific author",
    ),
]
