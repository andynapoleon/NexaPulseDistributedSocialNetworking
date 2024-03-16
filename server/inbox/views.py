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
from comments.serializers import CommentSerializerPost


# Create your views here.
class InboxView(APIView):

    def get(self, request, author_id, format=None):
        """
        Gets the inbox of the specified Author on a server.
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
        comment_serializer = CommentSerializerPost(inbox.comments.all(), many=True)
        response = {
            "type": "inbox",
            "author_id": author.id,
            "posts": posts_serializer.data,
            "comment_likes": comment_likes_serializer.data,
            "post_likes": post_likes_serializer.data,
            "follow_request": follow_serializer.data,
            "comments": comment_serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, author_id, format=None):
        """
        Adds something to the inbox of the specified Author on a server.
        """
        author = get_object_or_404(Author, pk=author_id)
        inbox, _ = Inbox.objects.get_or_create(authorId=author)
        request_type = request.data.get("type", "").lower()

        # Post
        if request_type == "post":
            post_id = request.data.pop("postId", None)
            existing_post = Post.objects.filter(id=post_id).first()
            if existing_post:
                for key, value in request.data.items():
                    setattr(existing_post, key, value)
                inbox.posts.add(existing_post)
            else:
                serializer = PostSerializer(data=request.data, partial=True)
                if serializer.is_valid():
                    new_post = serializer.save()
                inbox.posts.add(new_post)
            return Response(
                {"message": "Post sent to inbox!"}, status=status.HTTP_201_CREATED
            )

        # Follow requests
        elif request_type == "follow":
            follower_id = request.data.get("userId1")
            followed_id = request.data.get("userId2")
            if followed_id == author_id:
                follow = Follows(follower_id=follower_id, followed_id=followed_id)
                follow.save()
                inbox.follow_requests.add(follow)
                return Response(
                    {"message": "Follow request sent to inbox!"},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(
                    {"message": "Non-matching author to follow!"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        # Likes on posts
        elif request_type == "post_like":
            like = PostLikes.objects.create(
                author_id=request.data.get("author"), post_id=request.data.get("post")
            )
            inbox.post_likes.add(like)
            return Response(
                {"message": "Post like added to inbox!"}, status=status.HTTP_201_CREATED
            )

        # Comments
        elif request_type == "comment":
            serializer = CommentSerializerPost(data=request.data)
            new_comment = None
            if serializer.is_valid():
                new_comment = serializer.save()
            inbox.comments.add(new_comment)
            return Response(
                {"message": "Comment added to inbox!"}, status=status.HTTP_201_CREATED
            )

        # # Likes on comments
        elif request_type == "comment_like":
            like = CommentLikes.objects.create(
                author_id=request.data.get("author"), comment_id=request.data.get("comment"),
                post_id=request.data.get("post")
            )
            inbox.comment_likes.add(like)
            return Response(
                {"message": "Comment like added to inbox!"}, status=status.HTTP_201_CREATED
            )

        return Response(
            {"message": "Unsupported request type!"}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, author_id, format=None):
        """
        Deletes the inbox of the specified Author on a server.
        """
        author = get_object_or_404(Author, pk=author_id)
        inbox = get_object_or_404(Inbox, authorId=author)
        inbox.posts.clear()
        inbox.post_likes.clear()
        inbox.follow_requests.clear()
        inbox.comments.clear()
        inbox.comment_likes.clear()
        return Response(
            {"detail": f"Inbox of {author.firstName} deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
