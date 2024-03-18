from django.urls import path
from . import views

urlpatterns = [
    path('nodes/', views.NodeList.as_view(), name=('node-list')),
]
