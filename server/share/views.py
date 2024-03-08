from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics
from .models import SharedPost
from posts.models import Post
from .serializers import SharedPostSerializer


class SharePostAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, author_id, post_id):
        try:
            shared_posts = SharedPost.objects.filter(post=post_id, author=author_id)
            serializer = SharedPostSerializer(shared_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request, author_id, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if post.visibility == "PUBLIC" and int(author_id) != post.authorId.id:
            data = {"author": author_id, "post": post_id}
            serializer = SharedPostSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "You are not authorized to share this post"},
                status=status.HTTP_403_FORBIDDEN,
            )
