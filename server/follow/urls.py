from django.urls import path

from follow.views import (
    FollowView,
    FollowAllView,
    UserFollowingView,
    UserFollowedView,
    UserFriendsView,
    RemoteCheckFollow,
)

urlpatterns = [
    path("follow/<str:user_id>", FollowView.as_view()),
    path("follow/all/<str:user_id>", FollowAllView.as_view()),
    path("friends/following/<str:user_id>", UserFollowingView.as_view()),
    path("friends/followed/<str:user_id>", UserFollowedView.as_view()),
    path("friends/friends/<str:user_id>", UserFriendsView.as_view()),
    path(
        "authors/<str:author_id>/followers/<str:foreign_author_id>",
        RemoteCheckFollow.as_view(),
    ),
]
