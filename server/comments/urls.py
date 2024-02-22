from django.urls import path

from . import views # . referes to the current module we are in

urlpatterns = [
    path('authors/{AUTHOR_ID}/posts/{POST_ID}/comments', views.get_comment, name='get_comment'),
    path('service/api/author', views.create_comment, name='create_comment'),
]