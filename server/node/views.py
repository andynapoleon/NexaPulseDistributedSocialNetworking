from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from .models import Node
from .serializers import NodeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import base64
import requests
from .remote_functions import fetchRemoteAuthors


credentialForConnect = {
    "username": "hello",
    "password": "world",
}
credentialForDelete = {"", "", "", ""}


@api_view(["POST"])
@permission_classes((IsAuthenticatedOrReadOnly,))
def authRemoteNode(request, host):
    if request.META.get("HTTP_AUTHORIZATION") != None and "Basic" in request.META.get(
        "HTTP_AUTHORIZATION"
    ):
        auth_header = request.META["HTTP_AUTHORIZATION"]
        username, password = base64.b64decode(auth_header[6:]).split(":")
        if (
            username == credentialForConnect["username"]
            and password == credentialForConnect["password"]
        ):
            remoteNode = Node(host=host, username=host, password=host)
            remoteNode.save()
            response = {
                "username": remoteNode.username,
                "password": remoteNode.password,
            }
            return Response(response, status.HTTP_200_OK)
        response = {"message": "Incorrect Credentials"}
        return Response(response, status.HTTP_400_BAD_REQUEST)
    else:
        response = {"message": "Invalid Basic Auth"}
        return Response(response, status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getNode(request):
    remoteHost = request.GET.get("host")
    if remoteHost:
        try:
            nodes = Node.objects.get(host=remoteHost)
            serializer = NodeSerializer(nodes)
            if Node.DoesNotExist:
                response = {"error": "No such node exists"}
                return Response(response, status.HTTP_200_OK)
            else:
                response = serializer.data
                return Response(response, status.HTTP_200_OK)
        except:
            response = {
                "error": "Error occurred while fetching data from the database."
            }
            return Response(response, status.HTTP_503_SERVICE_UNAVAILABLE)
    else:
        response = {"error": "Please provide a valid hostname or IP address"}
        return Response(response, status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def getNodePosts(request):
    allPosts = []
    for node in Node.objects.all():
        remoteHost = node.host
        if remoteHost == None:
            response = {"error": "Please provide a valid hostname or IP address"}
            return Response(response, status.HTTP_200_OK)
        try:
            AuthorRequest = requests.request.get(
                f"http://{remoteHost}/authors/", auth={node.username, node.password}
            )
        except Exception as e:
            print(f"failed to get authors from {remoteHost}")
        if AuthorRequest.status_code != 200:
            response = {"error": "Couldn't connect to the specified server"}
            return Response(response, status.HTTP_200_OK)
        else:
            remoteAuthors = AuthorRequest.json().get("items")
            for author in remoteAuthors:
                try:
                    remoteAuthorPostsRequest = requests.request.get(
                        f"{author['id']}/posts/", auth={node.username, node.password}
                    )
                except Exception as e:
                    print(f"failed to get posts from author {author['id']}")

                if remoteAuthorPostsRequest.status_code != 200:
                    response = {"error": "Couldn't connect to the specified server"}
                    return Response(response, status.HTTP_200_OK)
                else:
                    remoteAuthorPosts = remoteAuthorPostsRequest.json().get("items")
                    allPosts.extend(remoteAuthorPosts)
    response = {"type": "posts", "items": allPosts}
    return Response(response, status.HTTP_200_OK)


@api_view(["GET"])
def getRemoteAuthors(request):
    remoteAuthors = fetchRemoteAuthors()
    response = {"type": "authors", "items": remoteAuthors}
    return Response(response, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def deleteNode(request, host):
    nodeToDelete = Node.objects.filter(host=host)[0]
    nodeToDelete.delete()
    response = {"message": "Node successfully deleted."}
    return Response(response, status=status.HTTP_200_OK)
