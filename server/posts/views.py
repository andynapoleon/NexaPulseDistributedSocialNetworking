from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

@api_view(['GET'])
def get_post(request, author_id, post_id):
    """
    Retrieve a single post by its ID.
    """
    try:
        post = Post.objects.get(id=post_id)
        author_id = post.author.id  # Access the author_id from the Post object
        
        serializer = PostSerializer(post)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response(status=404)
    
@api_view(['GET'])
def get_recent_posts(request, author_id):
    """
    Retrieve recent posts from a specific author.
    """
    try:
        posts = Post.objects.filter(author_id=author_id).order_by('-published')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    except Post.DoesNotExist:
        return Response(status=404)


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

@api_view(['DELETE'])
def delete_post(request, author_id, post_id):
    """
    Delete a specific post.
    """
    try:
        post = Post.objects.get(id=post_id, author_id=author_id)
        post.delete()
        return Response(status=204)
    except Post.DoesNotExist:
        return Response(status=404)