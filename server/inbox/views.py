from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authors.models import Author
from posts.models import Post
from follow.models import Follows
from follow.serializers import FollowsSerializer
from posts.serializers import PostSerializer
from likes.serializers import LikesSerializerComment, LikesSerializerPost
from .models import Inbox
from likes.models import PostLikes, CommentLikes
from comments.models import Comment
from comments.serializers import CommentSerializerPost
from auth.BasicOrTokenAuthentication import BasicOrTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from SocialDistribution.settings import SERVER
from node.models import Node
import requests


# Create your views here.
class InboxView(APIView):
    authentication_classes = [BasicOrTokenAuthentication]

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
        sender_host = request.query_params.get("request_host", None)

        # Post
        if request_type == "post":
            print("HERE", request.data)
            post_id = request.data.pop("postId", None)
            print("post_id", post_id)
            existing_post = Post.objects.filter(id=post_id).first()

            if existing_post:
                for key, value in request.data.items():
                    setattr(existing_post, key, value)
                inbox.posts.add(existing_post)
            else:
                author = Author.objects.get(id=request.data["authorId"])
                request.data["authorId"] = author
                if request.data["sharedBy"] != None:
                    request.data["sharedBy"] = Author.objects.get(
                        id=request.data["sharedBy"]
                    )
                id = request.data.pop("id")
                print("ID", id)
                image_ref = request.data.pop("image_ref", None)
                print("image ref", image_ref)
                # fetch the image from the server from authors/<str:author_id>/posts/<str:post_id>/image/
                if image_ref is not None and image_ref != "None":
                    url_image = (
                        f"{sender_host}api/authors/{author_id}/posts/{id}/image/"
                    )
                    node = Node.objects.all().filter(host=sender_host).first()
                    if not node:
                        node = Node.objects.all().filter(host=sender_host[0:-1]).first()
                    print("NODE:", node.username, node.password)
                    response = requests.get(
                        url_image,
                        auth=(node.username, node.password),
                        params={"request_host": SERVER},
                    ).json()
                    # pop image_id
                    image_id = response.pop("id")
                    image_id = image_id.split("/")[-2]
                    author_post = response.pop("authorId")
                    author_post = Author.objects.get(id=author_post)
                    response["authorId"] = author_post
                    response.pop("comments")
                    response.pop("author")
                    # create a image post instance
                    print("IMAGE ID", image_id)
                    print("ID", id)
                    if request.data["isShared"]:
                        image_ref = Post.objects.create(**response)
                    else:
                        image_ref = Post.objects.create(id=image_id, **response)
                    new_post = Post.objects.create(
                        id=id, image_ref=image_ref, **request.data
                    )
                else:
                    new_post = Post.objects.create(id=id, **request.data)
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
            post = Post.objects.get(id=request.data["postId"])
            author = Author.objects.get(id=request.data["author"])
            request.data["postId"] = post
            request.data["author"] = author
            id = request.data.pop("id")
            new_comment = Comment.objects.create(id=id, **request.data)
            inbox.comments.add(new_comment)
            return Response(
                {"message": "Comment added to inbox!"}, status=status.HTTP_201_CREATED
            )

        # Likes on comments
        elif request_type == "comment_like":
            print(request.data)
            like = CommentLikes.objects.create(
                author_id=request.data.get("author"),
                comment_id=request.data.get("comment"),
                post_id=request.data.get("post"),
            )
            inbox.comment_likes.add(like)
            return Response(
                {"message": "Comment like added to inbox!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": "Unsupported request type!"}, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, author_id, format=None):
        """
        Deletes the inbox of the specified Author on a server.
        """
        sender_host = request.query_params.get("request_host", None)
        author = get_object_or_404(Author, pk=author_id)
        inbox = get_object_or_404(Inbox, authorId=author)
        inbox.posts.clear()
        inbox.post_likes.clear()
        inbox.follow_requests.clear()
        inbox.comments.clear()
        inbox.comment_likes.clear()
        return Response(
            {"detail": f"Inbox of {author.displayName} deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
