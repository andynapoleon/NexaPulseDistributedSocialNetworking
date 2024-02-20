from django.urls import path, include
from . import views

urlpatterns = [
    path('get/', views.getData),
    path('add/', views.addAuthor),
    path("",include('posts.urls')),  # Include the posts app URLs
    path("",include('authors.urls')),  # Include the author app URLs
]