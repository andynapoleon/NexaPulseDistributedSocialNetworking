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
from node.models import Node
from node.serializers import NodeSerializer
from urllib.parse import urlparse
from rest_framework.permissions import AllowAny


def extract_uuid(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split("/")
    uuid = path_segments[-1]  # Assuming UUID is the last segment in the path
    return uuid


# Create your views here.
class InboxView(APIView):
    authentication_classes = [BasicOrTokenAuthentication] #BasicOrTokenAuthentication
    # permission_classes = [AllowAny]

    def convert_json(self, input_json):
        output_json = {
            "type": input_json["type"],
            "id": input_json["id"].split("/")[-1],  # Extracting the UUID from the URL
            "authorId": input_json["author"]["id"].split("/")[
                -1
            ],  # Extracting the UUID from the URL
            "title": input_json["title"],
            "content": input_json["content"],
            "contentType": input_json["contentType"],
            "visibility": input_json["visibility"],
            "source": input_json["source"],
            "image_ref": None,
            "sharedBy": None,
            "isShared": False,
        }
        try:
            output_json["image_ref"] = input_json["image_ref"].split("/")[-1]
        except:
            output_json["image_ref"] = None

        try:
            output_json["sharedBy"] = input_json["sharedBy"]
            output_json["isShared"] = input_json["isShared"]
        except KeyError:
            output_json["sharedBy"] = None
            output_json["isShared"] = False

        return output_json

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
        print("REQUEST DATA", request.data)
        print("AUTHOR ID", author_id)
        author = Author.objects.get(id=author_id)
        author.is_active = True
        author.save()
        # turn author to active

        inbox, _ = Inbox.objects.get_or_create(authorId=author)
        request_type = request.data.get("type", "").lower()
        sender_host = request.query_params.get("request_host", None)
        print(request_type)

        # Post
        if request_type == "post":
            print("POST REQUEST", request.data)
            request_data = self.convert_json(request.data)
            # {'type': 'post',
            # 'id': '43fb5f55-b492-4a11-b234-7b6ba5985b0e',
            # 'authorId': 'd491ceed-9c96-401e-8258-8fbadeddec13',
            # 'title': 'sss', 'content': 'ssss',
            # 'contentType': 'text/plain', 'visibility': 'PUBLIC',
            # 'source': 'http://127.0.0.1:8000/',
            # 'image_ref': 'None', 'sharedBy': None, 'isShared': False}

            image_ref = request_data.get("image_ref", None)
            print("IMAGE REF", image_ref)
            post_id = request_data["id"]

            print("POST ID", post_id)
            existing_post = Post.objects.filter(id=post_id).first()

            if existing_post:
                print("EXISTING POST", existing_post)

                if image_ref and image_ref != "None":
                    # fetch remote authors/${authorId}/posts/${postId}/image/",
                    url_image = (
                        f"{sender_host}api/authors/{author_id}/posts/{post_id}/image/"
                    )
                    node = Node.objects.all().filter(host=sender_host[0:-1]).first()
                    request_image = requests.get(
                        url_image,
                        auth=(node.username, node.password),
                        params={"request_host": SERVER},
                    ).json()
                    print("REQUEST IMAGE", request_image["id"].split("/")[6])
                    # update local image post
                    local_image_post = Post.objects.get(
                        id=request_image["id"].split("/")[6]
                    )
                    print(
                        type(local_image_post.content), type(request_image["content"])
                    )
                    local_image_post.content = request_image["content"]
                    local_image_post.save()

                local_data = {
                    "title": request_data["title"],
                    "content": request_data["content"],
                    "image": None,
                }

                # make put request to update the post
                # authors/<str:author_id>/posts/<str:post_id>
                url = (
                    SERVER
                    + f"api/authors/{request.data['author']['id'].split('/')[-1]}/posts/{post_id}/"
                )
                print("URLING", url)
                # use JWT token of the author
                access_token = author.token["access"]
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                }

                response = requests.put(
                    url,
                    json=local_data,
                    headers=headers,
                    params={"request_host": sender_host},
                )
                print("IBOX RESPONSE", response.json())
                # return the response
                return Response(response.json(), status=response.status_code)

            else:
                author = Author.objects.get(id=request_data["authorId"])
                request_data["authorId"] = author
                print("AUTHOR", type(request_data["authorId"]))
                if request_data["sharedBy"] != None:
                    request_data["sharedBy"] = Author.objects.get(
                        id=request_data["sharedBy"]
                    )
                id = request_data.pop("id")
                print("ID", id)
                image_ref = request_data.pop("image_ref", None)
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
                    if request_data["isShared"]:
                        image_ref = Post.objects.create(**response)
                    else:
                        image_ref = Post.objects.create(id=image_id, **response)
                    new_post = Post.objects.create(
                        id=id, image_ref=image_ref, **request_data
                    )
                else:
                    new_post = Post.objects.create(id=id, **request_data)
                inbox.posts.add(new_post)

            return Response(
                {"message": "Post sent to inbox!"}, status=status.HTTP_201_CREATED
            )

        # Follow requests
        elif request_type.lower() == "follow":
            print("IMHERERHEHRHERHEHRHEHR")
            print("HERE")
            print("REQUEST DATA", request.data["actor"], request.data["actor"])
            actor = request.data.get("actor")
            object = request.data.get("object")

            # Check if actor_id or object_id is a URL
            if "/" in actor["id"]:
                actor["id"] = extract_uuid(actor["id"])  # Extract UUID from URL
            if "/" in object["id"]:
                object["id"] = extract_uuid(object["id"])  # Extract UUID from URL

            follow = Follows.objects.filter(
                follower_id=actor["id"], followed_id=object["id"]
            )
            print(follow.exists())
            if follow.exists():
                follow.delete()
                return Response(
                    {"message": "Follow request sent to inbox!"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            print("ACTOR HOST: ", actor["host"])
            print("SERVER:", SERVER)
            if actor["host"][-1] != "/":
                actor["host"] += "/"
            if actor["host"] == SERVER:
                print("HOST HERE", object["host"])
                if object["host"][-1] == "/":
                    object["host"] = object["host"][0:-1]
                queryset = Node.objects.get(host=object["host"])
                serializer = NodeSerializer(queryset)
                node = serializer.data
                host = node["host"]
                actor_id = actor["id"]
                object_id = object["id"]
                actor_url = actor["url"]
                if "social-dist" in host:
                    print("GOING TO ALEX'S")
                    request_url = f"{host}/authors/{object_id}/followers/{actor_url}"
                else:
                    request_url = f"{host}/api/authors/{object_id}/followers/{actor_id}"
                response = requests.get(
                    request_url,
                    auth=(node["username"], node["password"]),
                    params={"request_host": actor["host"]},
                )
                print("status code", response.status_code)
                if response.status_code == 404:
                    return Response(
                        {"message": "Follow request rejected!"},
                        status=status.HTTP_200_OK,
                    )
                follow = Follows(
                    follower_id=actor["id"],
                    followed_id=object["id"],
                    acceptedRequest=True,
                )
            else:
                follow = Follows(follower_id=actor["id"], followed_id=object["id"])
            follow.save()
            inbox.follow_requests.add(follow)
            return Response(
                {"message": "Follow request sent to inbox!"},
                status=status.HTTP_201_CREATED,
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
