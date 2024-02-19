from django.urls import path
from . import views

urlpatterns = [
    path('authors/<str:author_id>/posts/<str:post_id>/', views.get_post, name='get_post'),
    path('authors/<str:author_id>/posts/', views.get_recent_posts, name='get_recent_posts'),
    # Add URL patterns for other operations (DELETE, PUT, POST) as needed
]