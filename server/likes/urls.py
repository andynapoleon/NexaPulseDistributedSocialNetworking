from django.urls import path
from . import views # . referes to the current module we are in

urlpatterns = [
    # Endpoint for likes for a specific post
    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/likes
    path("authors/<str:author_id>/posts/<str:post_id>/likes", views.PostLikeViewSet.as_view({'get': 'post_likes'}), name='get_post_likes'),
    # Endpoint for likes for a specific comment
    # URL: ://service/authors/{AUTHOR_ID}/posts/{POST_ID}/comments/{COMMENT_ID}/likes
    path("authors/<str:author_id>/posts/<str:post_id>/comments/<str:comment_id>/likes", views.CommentLikeViewSet.as_view({'get': 'comment_likes'}), name='get_comment_likes'),
    # Endpoint for sending a like to the author also deleting a like
    # URL: ://service/authors/{AUTHOR_ID}/inbox/
    path("authors/<str:author_id>/inbox", views.PostLikeViewSet.as_view({'post': 'like_post', 'delete': 'unlike_post'}), name='like_unlike_post'),
    path("authors/<str:author_id>/comment/inbox", views.CommentLikeViewSet.as_view({'post': 'like_comment', 'delete': 'unlike_comment'}), name='like_unlike_comment'),
    # Endpoint to get all the likes in a post
    path("authors/<str:author_id>/posts/<str:post_id>/listoflikes", views.PostLikeViewSet.as_view({'get': 'list_of_post'}), name='get_list_of_likes')
]