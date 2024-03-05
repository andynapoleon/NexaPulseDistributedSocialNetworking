from django.urls import path

from follow.views import FollowView, FollowAllView, UserFollowingView, UserFollowedView, UserFriendsView

urlpatterns = [
    path("api/follow/<int:user_id>", FollowView.as_view()),
    path("api/follow/all/<int:user_id>", FollowAllView.as_view()),
    path("api/friends/following/<int:user_id>", UserFollowingView.as_view()),
    path("api/friends/followed/<int:user_id>", UserFollowedView.as_view()),
    path("api/friends/friends/<int:user_id>", UserFriendsView.as_view()),

]