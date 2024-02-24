from django.urls import path, include
from . import views

urlpatterns = [
    # Endpoint for retrieving the list of posts
    path("posts/", views.PostList.as_view(), name="post_list"),
    # Endpoint for retrieving the list of posts
    path("public-posts/", views.PublicPosts.as_view(), name="post_list"),
    # Endpoint for retrieving a specific post by its author and post ID
    path(
        "authors/<str:author_id>/posts/<str:post_id>/",
        views.PostDetail.as_view(),
        name="get_post/update_post/delete_post",
    ),
    # Endpoint for retrieving recent posts by a specific author
    path(
        "authors/<str:author_id>/posts/",
        views.AuthorPosts.as_view(),
        name="get_author_posts/create_post",
    ),
    path(
        "authors/<str:author_id>/",
        views.ProfilePost.as_view(),
        name="get_profile_post",
    ),
]
