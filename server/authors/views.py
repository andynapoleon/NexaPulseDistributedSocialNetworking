from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author
from .serializers import AuthorSerializer

# We will not use this. Everything will be deligated to API

@api_view(['GET'])
def get_author(request):
    """
    Get the list of authors on our website
    """
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)