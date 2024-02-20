from django.urls import path

from . import views # . referes to the current module we are in

urlpatterns = [
    path('authors/authors/', views.get_author, name='get_author'),
]