from django.urls import path, include
from . import views

urlpatterns = [
    path('service/api/posts', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('service/api/authors/<str:author_id>/posts/<str:post_id>/', views.PostDetail.as_view(), name='get_post'),
    path('service/api/authors/<str:author_id>/posts/<str:post_id>/', views.PostDetail.as_view(), name='update_post'),
    path('service/api/authors/<str:author_id>/posts/', views.AuthorPosts.as_view(), name='get_recent_posts'),
    path('service/api/authors/<str:author_id>/posts/', views.AuthorPosts.as_view(), name='create_post'),  # URL for creating a post
]