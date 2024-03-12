from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models import Author
from authors.serializers import AuthorSerializer
from posts.models import Post
from follow.models import Follows
from follow.serializers import FollowsSerializer
from posts.serializers import PostSerializer
from likes.serializers import LikesSerializerComment
from likes.serializers import LikesSerializerPost
from .models import Inbox
from likes.models import PostLikes
from likes.models import CommentLikes
from comments.models import Comment
from comments.serializers import CommentSerializer


# Create your views here.
class InboxView(APIView):

    def get(self, request, author_id, format=None):
        """
        Retrieves all posts and likes from the inbox of the specified AppUser.
        """
        author = get_object_or_404(Author, pk=author_id)
        inbox = get_object_or_404(Inbox, authorId=author)

        # Serialize posts, likes, comments and follow requests
        posts_serializer = PostSerializer(
            inbox.posts.all().order_by("-published"), many=True
        )
        post_likes_serializer = LikesSerializerPost(inbox.post_likes.all(), many=True)
        comment_likes_serializer = LikesSerializerComment(
            inbox.comment_likes.all(), many=True
        )
        follow_serializer = FollowsSerializer(inbox.follow_requests.all(), many=True)
        comment_serializer = CommentSerializer(inbox.comments.all(), many=True)

        response = {
            "type": "inbox",
            "author_id": author.user_id,
            "posts": posts_serializer.data,
            "comment_likes": comment_likes_serializer.data,
            "post_likes": post_likes_serializer.data,
            "follow_request": follow_serializer.data,
            "comments": comment_serializer.data,
        }

        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, author_id, format=None):
        author = get_object_or_404(Author, pk=author_id)
        author_serializer = AuthorSerializer(author)
        author_name = author_serializer.data["firstName"]
        inbox, _ = Inbox.objects.get_or_create(authorId=author)

        request_type = request.data.get("type", "").lower()
        if request_type == "post":
            return Response({"add post to inbox here": author_name})
        elif request_type == "comment_like":
            return Response("add comment like to inbox here")
        elif request_type == "post_like":
            return Response("add post like to inbox here")
        elif request_type == "follow":
            return Response("add follow")

        return Response(
            {"detail": "Unsupported request type"}, status=status.HTTP_400_BAD_REQUEST
        )
