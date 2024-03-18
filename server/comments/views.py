from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Comment
from .serializers import CommentSerializer, CommentSerializerPost
from node.models import Node
import requests
from SocialDistribution.settings import SERVER
from auth.BasicOrTokenAuthentication import BasicOrTokenAuthentication


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentSerializerPost
        return CommentSerializer


class CommentDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentSerializerPost
        return CommentSerializer

    def get(self, request, author_id, post_id):
        try:
            comment = Comment.objects.filter(
                postId=post_id
            )  # get the comments of the post given post_id
            if (len(comment) == 0):
                return Response(status=status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        base_url = request.build_absolute_uri("/")
        serializer = self.get_serializer(
            comment, many=True, context={"base_url": base_url}
        )
        if serializer.is_valid:
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, author_id, post_id):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        # Check if the author_id provided in the URL matches the ID of the currently logged-in user
        if str(request.data.get("author")) != str(author_id):
            return Response(
                {
                    "error": "You are not authorized to post comments on behalf of other users."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Validate the serializer data
        if serializer.is_valid():
            serializer.save()

            remoteData = {
                "type": "comment",
                "id": serializer.data["id"],
                "content_type": request.data["content_type"],
                "comment": request.data["comment"],
                "author": request.data["author"],
                "postId": request.data["postId"],
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

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
