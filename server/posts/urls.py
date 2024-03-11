from django.urls import path, include
from . import views

urlpatterns = [
    # Endpoint for retrieving the list of posts
    path("posts/", views.PostList.as_view(), name="post_list"),
    # Endpoint for retrieving a post by id
    path(
        "authors/<str:author_id>/posts/<str:post_id>/",
        views.PostDetail.as_view(),
        name="post_detail",
    ),
    # Endpoint for retrieving the list of posts with an image
    path(
        "authors/<str:author_id>/posts/<str:post_id>/image/",
        views.PostDetail.as_view(),
        name="image_post_detail",
    ),
    # Endpoint for retrieving the list of posts
    path("public-posts/", views.PublicPosts.as_view(), name="public_post_list"),
    # Endpoint for retrieving the list of posts of people we're following
    path("following-posts/", views.FollowingPosts.as_view(), name="following_post_list"),
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
        "authors/posts/<str:author_id>/",
        views.ProfilePost.as_view(),
        name="get_profile_post",
    ),
    # Endpoint for retrieving recent posts by a specific author as a stranger
    path(
        "authors/posts/<str:author_id>/asStranger",
        views.ProfilePostForStranger.as_view(),
        name="get_profile_post_as_strangers",
    ),
    # Endpoint for retrieving recent posts by a specific author as the user himself
    path(
        "authors/posts/<str:author_id>/asHimself",
        views.ProfilePostForHimself.as_view(),
        name="get_profile_post_as_himself",
    ),
    # Endpoint for sharing posts
    path(
        "authors/<str:author_id>/shared-posts/<str:post_id>/",
        views.SharedPost.as_view(),
        name="share-post",
    ),
]
