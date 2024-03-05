from django.urls import path, include
from . import views
from auth.views import LoginView, TokenRefreshAPIView
from authors.views import Profile
from follow.views import FollowView, FollowAllView, UserFollowingView, UserFollowedView, UserFriendsView

urlpatterns = [
    path('api/get/', views.getData),
    path('api/profile/<int:user_id>', Profile.as_view(), name="Profile"),
    path('api/add/', views.addAuthor),
    path("api/token/", LoginView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("api/",include('posts.urls')),  # Include the posts app URLs
    path("api/",include('authors.urls')),  # Include the author app URLs
    path("api/",include('comments.urls')), # Include the comments app URLs
    path("api/", include('follow.views')), # Include the follow app URLS
]