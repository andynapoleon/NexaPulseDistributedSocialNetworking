from django.urls import path, include
from . import views

# urlpatterns = [
#     path('GET/post_list', views.PostList.as_view()),
#     path('posts/<int:pk>/', views.PostDetail.as_view()),
#     path('GET/authors/<str:author_id>/posts/<str:post_id>/', views.PostDetail.as_view(), name='get_post'),
#     path('PUT/authors/<str:author_id>/posts/<str:post_id>/', views.PostDetail.as_view(), name='update_post'),
#     path('GET/authors/<str:author_id>/posts/', views.AuthorPosts.as_view(), name='get_recent_posts'),
#     path('PUT/api/authors/<str:author_id>/posts/', views.AuthorPosts.as_view(), name='create_post'),  # URL for creating a post
# ]

urlpatterns = [
    # Endpoint for retrieving the list of posts
    path('posts/', views.PostList.as_view(), name='post_list'),

    # Endpoint for retrieving a specific post by its author and post ID
    path('authors/<str:author_id>/posts/<str:post_id>/', views.PostDetail.as_view(), name='get_post/update_post/delete_post'),

    # Endpoint for retrieving recent posts by a specific author
    path('authors/<str:author_id>/posts/', views.AuthorPosts.as_view(), name='get_author_posts/create_post'),
]