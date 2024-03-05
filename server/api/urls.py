from django.urls import path, include
from . import views
from auth.views import LoginView, TokenRefreshAPIView
from authors.views import Profile
from follow.views import (
    FollowView,
    FollowAllView,
    UserFollowingView,
    UserFollowedView,
    UserFriendsView,
)

urlpatterns = [
    path("api/get/", views.getData),
    path("api/profile/<int:user_id>", Profile.as_view(), name="Profile"),
    path("api/add/", views.addAuthor),
    path("api/token/", LoginView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("api/", include("posts.urls")),  # Include the posts app URLs
    path("api/", include("authors.urls")),  # Include the author app URLs
    path("api/", include("comments.urls")),  # Include the comments app URLs
    path("api/", include("share.urls")),  # Include the share app URLs
    path("api/follow/<int:user_id>", FollowView.as_view()),
    path("api/follow/all/<int:user_id>", FollowAllView.as_view()),
    path("api/friends/following/<int:user_id>", UserFollowingView.as_view()),
    path("api/friends/followed/<int:user_id>", UserFollowedView.as_view()),
    path("api/friends/friends/<int:user_id>", UserFriendsView.as_view()),
]
