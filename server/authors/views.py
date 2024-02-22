from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Author
from .serializers import AuthorSerializer
from rest_framework import generics

class AuthorList(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

@api_view(['GET'])
def get_author(request):
    """
    Get the list of authors on our website
    """
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_author(request):
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


