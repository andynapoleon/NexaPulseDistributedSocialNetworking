from .models import Node
from .serializers import NodeSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import base64
import requests
import json
from authors.models import Author


def fetchRemoteAuthors():
    allAuthors = []
    node = Node.objects.first()
    if node:
        remoteHost = node.host
        if not remoteHost:
            return allAuthors
        request_url = f"{remoteHost}api/authors/"
        try:
            response = requests.get(request_url, auth=(node.username, node.password))
            if response.status_code == 200:
                remoteAuthors = response.json().get("items", [])
                print("remote authors", json.dumps(response.json(), indent=4))
                for author in remoteAuthors:
                    user_id = author.get("id")
                    print("author data", author)
                    defaults = {
                        "email": author.get("email"),
                        "firstName": author.get("firstName"),
                        "lastName": author.get("lastName"),
                        "github": author.get("github"),
                        "profileImage": author.get("profileImage"),
                        "host": author.get("host"),
                        "isForeign": True,
                    }
                    Author.objects.update_or_create(user_id=user_id, defaults=defaults)
                    allAuthors.append(author)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching authors from {remoteHost}: {e}")
            return allAuthors
    return allAuthors
