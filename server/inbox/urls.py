from django.urls import path
from .views import InboxView

urlpatterns = [
    path("authors/<int:author_id>/inbox/", InboxView.as_view(), name="inbox"),
]
