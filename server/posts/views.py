from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def get_post(request, author_id):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True) # Many serializations
    return Response(serializer.data)

@api_view(['POST'])
def create_post(request, author_id):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET','POST'])
def update_post(request, author_id, post_id):
    post = Post.objects.get(id=post_id)
    serializer = PostSerializer(post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(status=400, data=serializer.errors)