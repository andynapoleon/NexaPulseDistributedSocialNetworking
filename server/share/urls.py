from django.urls import path
from .views import SharePostAPIView

urlpatterns = [
    path("share/shared-post/", SharePostAPIView.as_view(), name="shared-post-details"),
    path("share/share-post/", SharePostAPIView.as_view(), name="share_post"),
]
