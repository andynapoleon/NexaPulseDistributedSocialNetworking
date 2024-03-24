from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CommentLikes, PostLikes
from .serializers import LikesSerializerComment, LikesSerializerPost
from node.models import Node
import requests
from SocialDistribution.settings import SERVER
from auth.BasicOrTokenAuthentication import BasicOrTokenAuthentication
from authors.models import Author
from authors.serializers import AuthorSerializer


class PostLikeViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicOrTokenAuthentication]

    queryset = PostLikes.objects.all()
    serializer_class = LikesSerializerPost
    lookup_field = "post_id"

    @action(detail=True, methods=["get"])
    def list_of_post(self, request, author_id, post_id):
        # Query to retrieve likes on the specified post excluding the likes made by the post author
        likes = PostLikes.objects.filter(post_id=post_id)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["get"])
    def post_likes(self, request, author_id, post_id):
        # Query to retrieve likes on the specified post excluding the likes made by the post author
        likes = PostLikes.objects.filter(post_id=post_id).exclude(author_id=author_id)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=["post"])
    def like_post(self, request, author_id=None, post_id=None):
        serializer = self.get_serializer(data=request.data)
        print("I'm in local post like")
        try:
            like = PostLikes.objects.create(
                author_id=author_id, post_id=request.data.get("post")
            )
            base_url = request.build_absolute_uri("/")
            serializer = self.get_serializer(like, context={"base_url": base_url})

            # remoteData = {
            #     "type": "post_like",
            #     "author": author_id,
            #     "post": request.data["post"],
            # }

            remoteData = serializer.data
            print("SERIALIZER LIKE THIS ", serializer.data)

            # get all nodes
            node = Node.objects.all().filter(isActive=True)
            print("URL", node)
            for n in node:
                print("URL", n.host)
                print("POST's AUTHOR ID", request.data["author"])
                print("POST ID", post_id)
                if "social-dist" in n.host:
                    url = n.host + f"/authors/{request.data['author']}/inbox"
                else:
                    url = n.host + f"/api/authors/{request.data['author']}/inbox"
                response = requests.post(
                    url,
                    json=remoteData,
                    auth=(n.username, n.password),
                    params={"request_host": SERVER},
                )
                print("status code", response.status_code)
                if response.status_code == 201:
                    return Response(serializer.data, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=False, methods=["delete"])
    def unlike_post(self, request, author_id=None, post_id=None):
        print("I'm in local unlike", request.data)
        if str(request.data.get("author")) != author_id:
            return Response(
                {
                    "error": "You are not authorized to unlike posts on behalf of other users."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            like = PostLikes.objects.get(
                author_id=author_id, post_id=request.data.get("post")
            )
            like.delete()

            remoteData = {
                "author": request.data["author"],
                "post": request.data["post"],
            }

            # get all nodes
            query_set = Author.objects.get(id=author_id)
            serializer = AuthorSerializer(query_set)
            author = serializer.data
            if author["host"] == SERVER:
                node = Node.objects.all()
                for n in node:
                    url = n.host + f"/api/authors"
                    print("URL", url)
                    response = requests.get(
                        url,
                        auth=(n.username, n.password),
                        params={"request_host": SERVER},
                    )

                    url = n.host + f"/api/authors/{author_id}/inbox"
                    response = requests.delete(
                        url,
                        json=remoteData,
                        auth=(n.username, n.password),
                        params={"request_host": SERVER},
                    )
                    print(response)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PostLikes.DoesNotExist:
            return Response(
                {"error": "The specified like does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )


class CommentLikeViewSet(viewsets.ModelViewSet):
    permission_class = [IsAuthenticated]

    queryset = CommentLikes.objects.all()
    serializer_class = LikesSerializerComment
    lookup_field = "comment_id"

    @action(detail=True, methods=["get"])
    def comment_likes(self, request, author_id=None, post_id=None, comment_id=None):
        # Check if the comment is from post of post_id
        try:
            comment = CommentLikes.objects.filter(comment_id=comment_id)
        except CommentLikes.DoesNotExist:
            return Response(status=404)

        # if comment.post_id != post_id:
        #     return Response(status=404)

        # Query to retrieve likes on the specified comment excluding the likes made by the author who posted
        likes = CommentLikes.objects.filter(
            post_id=post_id, comment_id=comment_id
        ).exclude(author_id=author_id)
        serializer = self.get_serializer(likes, many=True)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=["post"])
    def like_comment(self, request, author_id=None, post_id=None, comment_id=None):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        # Check if the author_id provided in the URL matches the ID of the currently logged-in user
        if str(request.data.get("author")) != str(author_id):
            return Response(
                {
                    "error": "You are not authorized to like posts on behalf of other users."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            like = CommentLikes.objects.create(
                author_id=author_id,
                post_id=request.data.get("post"),
                comment_id=request.data.get("comment"),
            )
            base_url = request.build_absolute_uri("/")
            serializer = self.get_serializer(like, context={"base_url": base_url})

            remoteData = {
                "type": "comment_like",
                "author": author_id,
                "post": request.data["post"],
                "comment": request.data["comment"],
            }

            # get all nodes
            node = Node.objects.all()
            for n in node:
                url = n.host + f"/api/authors"
                print("URL", url)
                response = requests.get(
                    url,
                    auth=(n.username, n.password),
                    params={"request_host": SERVER},
                )

                url = n.host + f"/api/authors/{author_id}/inbox/"
                response = requests.post(
                    url,
                    json=remoteData,
                    auth=(n.username, n.password),
                    params={"request_host": SERVER},
                )
                print(response)

            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

    @action(detail=False, methods=["delete"])
    def unlike_comment(self, request, author_id=None, post_id=None, comment_id=None):
        print(request.data)
        if str(request.data.get("author")) != str(author_id):
            return Response(
                {
                    "error": "You are not authorized to unlike posts on behalf of other users."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            like = CommentLikes.objects.get(
                author_id=author_id,
                post_id=request.data.get("post"),
                comment_id=request.data.get("comment"),
            )
            like.delete()

            remoteData = {
                "author": request.data["author"],
                "post": request.data["post"],
                "comment": request.data["comment"],
            }

            # get all nodes
            query_set = Author.objects.get(id=author_id)
            serializer = AuthorSerializer(query_set)
            author = serializer.data
            if author["host"] == SERVER:
                node = Node.objects.all()
                for n in node:
                    url = n.host + f"/api/authors"
                    print("URL", url)
                    response = requests.get(
                        url,
                        auth=(n.username, n.password),
                        params={"request_host": SERVER},
                    )

                    url = n.host + f"/api/authors/{author_id}/comment/inbox"
                    response = requests.delete(
                        url,
                        json=remoteData,
                        auth=(n.username, n.password),
                        params={"request_host": SERVER},
                    )
                    print(response)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CommentLikes.DoesNotExist:
            return Response(
                {"error": "The specified like does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=True, methods=["get"])
    def list_of_comment_likes(self, request, author_id, post_id, comment_id):
        try:
            # Query to retrieve likes on the specified comment
            likes = CommentLikes.objects.filter(post_id=post_id, comment_id=comment_id)
            serializer = self.get_serializer(likes, many=True)
            return Response(serializer.data, status=200)
        except CommentLikes.DoesNotExist:
            return Response(
                {"error": "No likes found for the specified comment."},
                status=status.HTTP_404_NOT_FOUND,
            )
