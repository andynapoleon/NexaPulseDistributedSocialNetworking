from django.urls import path

from . import views # . referes to the current module we are in

urlpatterns = [
    path('authors/authors/', views.get_author, name='get_author'),
    path('service/api/author', views.AuthorList.as_view(), name='Author List'),
    path('author/<int:pk>/', views.AuthorDetail.as_view()),
    path('authors/create_author_test', views.create_author, name='post_author'),
]