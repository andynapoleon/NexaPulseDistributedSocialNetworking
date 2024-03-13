from django.urls import path

from . import views # . referes to the current module we are in

urlpatterns = [
    path('authors/', views.AuthorList.as_view(), name='Author List'),
    path('authors/<str:author_id>/', views.AuthorDetail.as_view(), name='Get specific author'),
]