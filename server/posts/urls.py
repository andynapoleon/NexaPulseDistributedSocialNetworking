from django.urls import path, include
from . import views

urlpatterns = [
    path('service/api/authors/authors/<str:author_id>/posts/<str:post_id>/', views.get_post, name='get_post'),
    path('service/api/authors/authors/<str:author_id>/posts/', views.get_recent_posts, name='get_recent_posts'),
    path('service/api/authors/<str:author_id>/posts/', views.create_post, name='create_post'),
    path('service/api/authors/<str:author_id>/posts/<str:post_id>', views.update_post, name='update_post'),
]