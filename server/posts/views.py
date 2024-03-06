from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Post
from .serializers import PostSerializer
from follow.models import Follows


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by("-published")
    serializer_class = PostSerializer


class ProfilePost(generics.ListCreateAPIView):
    permission_classes = [AllowAny]

    def get(self, request, author_id):
        try:
            # Filter posts by author ID
            posts = Post.objects.filter(authorId=author_id).order_by("-published")

            # Serialize the queryset to JSON
            serializer = PostSerializer(posts, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)
        except Exception as e:
            # Handle exceptions (e.g., author not found, serializer errors)
            return Response({"error": str(e)}, status=500)


class PostDetail(APIView):
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        return PostSerializer

    def get(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id)
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                if request.user.id == int(author_id):
                    serializer.save()
                    return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, author_id, post_id):
        # Retrieve the post object
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.user.id == int(author_id):
            # Delete the post
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_403_FORBIDDEN)


class AuthorPosts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        posts = Post.objects.filter(authorId=author_id).order_by("-published")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, author_id):
        serializer = PostSerializer(data=request.data)
        print(serializer.initial_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicPosts(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Filter posts by authorId and visibility='PUBLIC'
        posts = Post.objects.filter(visibility="PUBLIC").order_by("-published")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class FollowingPosts(APIView):
    def get(self, request):
        try:
            user_id = request.user.id

            # Get posts authored by users the current user follows
            followed_users_ids = Follows.objects.filter(
                follower_id=user_id, acceptedRequest=True
            ).values_list("followed_id", flat=True)

            # Include the current user's ID in the list of followed users
            followed_users_ids = list(followed_users_ids)
            followed_users_ids.append(user_id)

            queryset = Post.objects.filter(
                visibility="PUBLIC", authorId__in=followed_users_ids
            ).order_by("-published")

            # Order by published date
            queryset = queryset.order_by("-published")

            # Serialize the queryset to JSON
            serializer = PostSerializer(queryset, many=True)

            # Return serialized data as JSON response
            return Response(serializer.data)

        except Exception as e:
            # Handle exceptions (e.g., author not found, serializer errors)
            return Response({"error": str(e)}, status=500)
