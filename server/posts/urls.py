from django.urls import path, include
from . import views

urlpatterns = [
    path('service/api/authors/<str:author_id>/posts/', views.get_post, name='get_post'),
    path('service/api/authors/<str:author_id>/posts/', views.create_post, name='create_post'),
    path('service/api/authors/<str:author_id>/posts/<str:post_id>', views.update_post, name='get_post'),
]