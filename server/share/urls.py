from django.urls import path
from .views import SharePostAPIView

urlpatterns = [
    path(
        "authors/<str:author_id>/shared-posts/<str:post_id>/",
        SharePostAPIView.as_view(),
        name="share-post",
    ),
]
