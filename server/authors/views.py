from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Authors
from .serializers import AuthorsSerializer

# We will not use this. Everything will be deligated to API

@api_view(['GET'])
def get_authors(request):
    """
    Get the list of authors on our website
    """
    authors = Authors.objects.all()
    serializer = AuthorsSerializer(authors, many=True)
    return Response(serializer.data)