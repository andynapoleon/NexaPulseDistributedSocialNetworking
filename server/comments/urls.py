from django.urls import path

from . import views # . referes to the current module we are in

# path('authors/<str:author_id>/posts/<str:post_id>/comments/', views.CommentList.as_view(), name='comment-list'),

urlpatterns = [
    path('authors/<str:author_id>/posts/<str:post_id>/comments', views.get_comment, name='get_comment'),
    #path('service/api/author', views.create_comment, name='create_comment'),
]