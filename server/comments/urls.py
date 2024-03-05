from django.urls import path
from . import views # . referes to the current module we are in

# path('authors/<str:author_id>/posts/<str:post_id>/comments/', views.CommentList.as_view(), name='comment-list'),

urlpatterns = [
    # Endpoint for retrieving comments for a specific post
    path("authors/<str:author_id>/posts/<str:post_id>/comments", views.CommentDetail.as_view(), name="get_comments"),
]