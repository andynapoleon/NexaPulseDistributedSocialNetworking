from django.urls import path, include
from . import views

urlpatterns = [
    path('authors/test_author_id/posts/test_post_id/test_get', views.get_post, name='get_post'),
    path('authors/test_author_id/posts/test_post_id/test_post', views.create_post)
    # Add URL patterns for other operations (DELETE, PUT, POST) as needed
]