from django.urls import path, include
from . import views
from auth.views import LoginView, TokenRefreshAPIView
from follow.views import FollowView, FollowAllView

urlpatterns = [
    path('api/get/', views.getData),
    path('api/profile/<int:user_id>', views.Profile.as_view()),
    path('api/add/', views.addAuthor),
    path("api/token/", LoginView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("api/",include('posts.urls')),  # Include the posts app URLs
    path("api/",include('authors.urls')),  # Include the author app URLs
    path("api/follow/<int:user_id>", FollowView.as_view()),
    path("api/follow/all/<int:user_id>", FollowAllView.as_view()),
]