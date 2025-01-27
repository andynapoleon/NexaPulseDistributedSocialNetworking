from django.urls import path, include
from . import views
from auth.views import LoginView, TokenRefreshAPIView
from authors.views import Profile

urlpatterns = [
    path("api/get/", views.getData),
    path("api/profile/<str:user_id>", Profile.as_view(), name="Profile"),
    path("api/add/", views.addAuthor),
    path("api/token/", LoginView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("api/", include("posts.urls")),  # Include the posts app URLs
    path("api/", include("authors.urls")),  # Include the author app URLs
    path("api/", include("comments.urls")),  # Include the comments app URLs
    path("api/", include("follow.urls")),  # Include the follow app URLS
    path("api/", include("likes.urls")),  # Include the likes app URLS
    path("api/", include("node.urls")),  # Include the likes app URLS
    path("api/", include("inbox.urls")),  # Include the likes app URLS
    path("api/", include("node.urls")),  # Include the node app URLS
]
