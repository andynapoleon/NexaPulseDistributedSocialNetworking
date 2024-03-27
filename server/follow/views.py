from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from authors.models import Author
from authors.serializers import AuthorSerializer
from follow.models import Follows
from rest_framework.decorators import api_view
from .serializers import FollowsSerializer
from rest_framework.decorators import action
import requests
from node.models import Node
from node.serializers import NodeSerializer
from django.core.exceptions import ObjectDoesNotExist
from SocialDistribution.settings import SERVER
from auth.BasicOrTokenAuthentication import BasicOrTokenAuthentication
from rest_framework import generics
from urllib.parse import urlparse


def extract_uuid(url):
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split("/")
    uuid = path_segments[-1]  # Assuming UUID is the last segment in the path
    return uuid


class FollowView(APIView):
    authentication_classes = [BasicOrTokenAuthentication]  # [IsAuthenticated]

    def put(self, request, user_id):
        userId1 = request.data.get("userId1")
        userId2 = request.data.get("userId2")
        query_set = Author.objects.get(id=userId1)
        serializer = AuthorSerializer(query_set)
        following_author = serializer.data
        # remote
        if following_author["host"] != SERVER:
            print("REMOTE!!!!!!!")
            if following_author["host"][-1] == "/":
                following_author["host"] = following_author["host"][0:-1]
            print(following_author["host"])
            queryset = Node.objects.all().first()
            serializer = NodeSerializer(queryset)
            node = serializer.data
            print(node["host"] + " " + node["username"] + " " + node["password"])
            queryset = Node.objects.get(host=following_author["host"])
            serializer = NodeSerializer(queryset)
            node = serializer.data
            host = node["host"]
            print("FOLLOWING HOST:", host)
            if "social-dist" in host:
                request_url = f"{host}/authors/{userId1}/inbox"
            else:
                request_url = f"{host}/api/authors/{userId1}/inbox"
            print(request_url)
            try:
                actor = Author.objects.get(id=request.data["userId1"])
                actor = AuthorSerializer(actor)
                object = Author.objects.get(id=request.data["userId2"])
                object = AuthorSerializer(object)
                data_to_send = {
                    "type": "Follow",
                    "summary": str(actor.data["displayName"])
                    + " wants to follow "
                    + str(object.data["displayName"]),
                    "actor": actor.data,
                    "object": object.data,
                }
                # data_to_send = {
                #     "type": "Follow",
                #     "summary": str(actor.data["displayName"])
                #     + " wants to follow "
                #     + str(object.data["displayName"]),
                #     "actor": "fdasfdas",
                #     "object": "fadsfdsf",
                # }
                print("DATA TO SEND", data_to_send)
                requestObj = Follows.objects.filter(
                    follower_id=userId1, followed_id=userId2
                ).first()
                if requestObj:
                    requestObj.acceptedRequest = True
                requestObj.save()
                print("REQUEST URL", request_url)
                response = requests.post(
                    request_url,
                    json=data_to_send,
                    auth=(node["username"], node["password"]),
                    params={"request_host": SERVER},
                )
                print("status code response", response.status_code)
                if response.status_code in [200, 201, 204]:
                    return Response(
                        {"success": "Succeeded accepting follow request"},
                        status=status.HTTP_200_OK,
                    )
            except requests.exceptions.RequestException as e:
                return Response(
                    {"error": f"Couldnt sent friend request to remote inbox: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        # local
        else:
            if userId1 == userId2:
                return Response(
                    {"error": "UserId2 and UserId1 must be unique"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not (userId2):
                return Response(
                    {"error": "UserId2 must be provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            requestObj = Follows.objects.filter(
                follower_id=userId1, followed_id=userId2
            ).first()

            if requestObj:
                requestObj.acceptedRequest = True
                requestObj.save()
            else:
                return Response(
                    {"error": "Request does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"success": "Follow request accepted"}, status=status.HTTP_200_OK
            )

    def post(self, request, user_id):
        sender_host = request.data.get("senderHost")
        receiver_host = request.data.get("receiverHost")[0:-1]
        if sender_host[-1] == "/":
            sender_host = sender_host[0:-1]
        if receiver_host[-1] == "/":
            receiver_host = receiver_host[0:-1]
        print("SENDER", sender_host)
        print("RECEIVE", receiver_host)
        # remote
        if sender_host != receiver_host:
            userId2 = request.data.get("userId2")
            print("HOST", receiver_host)
            # print("ALL", Node.objects.all().first())
            queryset = Node.objects.get(host=receiver_host)
            print("FIRST", queryset)
            print("fdafajdfhjksdfhas")
            serializer = NodeSerializer(queryset)
            node = serializer.data
            host = node["host"]
            if "social-dist" in host:
                request_url = f"{host}/authors/{userId2}/inbox"
            else:
                request_url = f"{host}/api/authors/{userId2}/inbox"
            try:
                actor = Author.objects.get(id=request.data["userId1"])
                actor = AuthorSerializer(actor)
                object = Author.objects.get(id=request.data["userId2"])
                object = AuthorSerializer(object)
                data_to_send = {
                    "type": "Follow",
                    "summary": str(actor.data["displayName"])
                    + " wants to follow "
                    + str(object.data["displayName"]),
                    "actor": actor.data,
                    "object": object.data,
                }
                response = requests.post(
                    request_url,
                    json=data_to_send,
                    auth=(node["username"], node["password"]),
                    params={"request_host": sender_host},
                )
                print("status code response", response.status_code)
                if response.status_code == 201:
                    return Response(
                        {"success": "Succeeded sending follow request"},
                        status=status.HTTP_200_OK,
                    )
            except requests.exceptions.RequestException as e:
                return Response(
                    {"error": f"Couldnt sent friend request to remote inbox: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        # local
        else:
            userId2 = request.data.get("userId2")
            if user_id == userId2:
                return Response(
                    {"error": "UserId2 and UserId1 must be unique"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not (userId2):
                return Response(
                    {"error": "UserId2 must be provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            follow = Follows(follower_id=user_id, followed_id=userId2)
            follow.save()
            return Response(
                {"success": "Now following userId2"}, status=status.HTTP_200_OK
            )

    def delete(self, request, user_id):
        # local
        user_being_follow_id = request.query_params.get("userId2")
        if not (user_being_follow_id):
            return Response(
                {"error": "UserId2 must be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        Follows.objects.filter(
            followed_id=user_being_follow_id, follower_id=user_id
        ).delete()
        print("DELETING THIS SHIT")
        # remote
        query_set = Author.objects.get(id=user_id)
        serializer = AuthorSerializer(query_set)
        following_author = serializer.data
        if following_author["host"][-1] != "/":
            following_author["host"] += "/"
        if following_author["host"] == SERVER:
            query_set = Author.objects.get(id=user_being_follow_id)
            serializer = AuthorSerializer(query_set)
            following_author = serializer.data
        print("FOLLOWING AUTHOR HERE!", following_author)
        userId1 = request.data.get("userId1")
        userId2 = request.data.get("userId2")
        try:
            if following_author["host"][-1] == "/":
                following_author["host"] = following_author["host"][0:-1]
            print("TRYING IN HERE")
            queryset = Node.objects.get(host=following_author["host"])
        except:
            return Response({"success": "Deleted"}, status=status.HTTP_204_NO_CONTENT)
        serializer = NodeSerializer(queryset)
        node = serializer.data
        host = node["host"]
        print("MADE IT HERE")
        if "social-dist" in host:
            print("MADE IT HERE TOOO")
            request_url = f"{host}/authors/{userId1}/inbox"
        else:
            request_url = f"{host}/api/authors/{userId1}/inbox"
        # request_url = f"{host}/api/authors/{userId1}/inbox/"
        try:
            actor = Author.objects.get(id=request.data["userId1"])
            actor = AuthorSerializer(actor)
            object = Author.objects.get(id=request.data["userId2"])
            object = AuthorSerializer(object)
            data_to_send = {
                "type": "Follow",
                "summary": str(actor.data["displayName"])
                + " wants to follow "
                + str(object.data["displayName"]),
                "actor": actor.data,
                "object": object.data,
            }
            print("DATA_TO_SEND", data_to_send)
            print("MADE IT HERE")
            response = requests.post(
                request_url,
                json=data_to_send,
                auth=(node["username"], node["password"]),
                params={"request_host": SERVER},
            )
            print("status code response", response.status_code)
            if response.status_code in [200, 201, 204]:
                return Response(
                    {"success": "Succeeded rejecting follow request"},
                    status=status.HTTP_200_OK,
                )
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Couldnt sent friend request to remote inbox: {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"success": "Unfollowed userId2"}, status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, user_id):
        target_user_id = request.query_params.get("userId2")
        if not (target_user_id):
            return Response(
                {"error": "UserId2 must be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        requestObj = Follows.objects.filter(
            followed_id=user_id, follower_id=target_user_id
        ).first()
        if requestObj:
            follow_exists = True
            accepted_request = requestObj.acceptedRequest
        else:
            follow_exists = False
            accepted_request = None
        return Response(
            {"following": follow_exists, "acceptedRequest": accepted_request},
            status=status.HTTP_200_OK,
        )


class FollowAllView(APIView):
    permission_classes = [IsAuthenticated]  # [IsAuthenticated]

    def get(self, request, user_id):
        followers = Follows.objects.filter(followed_id=user_id)
        serializer = FollowsSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFollowingView(APIView):
    permission_classes = [IsAuthenticated]  # [IsAuthenticated]

    def get(self, request, user_id):
        return_package = []
        followings = Follows.objects.filter(follower_id=user_id, acceptedRequest=True)
        serializer = FollowsSerializer(followings, many=True)

        for followingUser in serializer.data:

            user = Author.objects.get(id=followingUser["followed"])
            if not user:
                return Response({"error": "User not found"}, status=404)

            user_id = user.id
            full_name = f"{user.displayName}"
            profileImage = user.profileImage  # Need to solve
            email = user.email
            context = {
                "user_id": user_id,
                "full_name": full_name,
                "profileImage": profileImage,
                "email": email,
            }
            return_package.append(context)
        return Response(return_package)


class UserFollowedView(APIView):
    authentication_classes = [BasicOrTokenAuthentication]  # [IsAuthenticated]

    def get(self, request, user_id):
        return_package = []
        followeds = Follows.objects.filter(followed_id=user_id, acceptedRequest=True)
        serializer = FollowsSerializer(followeds, many=True)

        for followedUser in serializer.data:

            user = Author.objects.get(id=followedUser["follower"])
            if not user:
                return Response({"error": "User not found"}, status=404)

            user_id = user.id
            full_name = f"{user.displayName}"
            profileImage = user.profileImage  # Need to solve
            email = user.email
            context = {
                "user_id": user_id,
                "full_name": full_name,
                "profileImage": profileImage,
                "email": email,
            }
            return_package.append(context)
        return Response(return_package)


class UserFriendsView(APIView):
    authentication_classes = [BasicOrTokenAuthentication]  # [IsAuthenticated]

    def get(self, request, user_id):

        return_package = []
        friendIdList = []
        followeds = Follows.objects.filter(followed_id=user_id, acceptedRequest=True)
        followings = Follows.objects.filter(follower_id=user_id, acceptedRequest=True)

        followedsSerializer = FollowsSerializer(followeds, many=True)
        followingsSerializer = FollowsSerializer(followings, many=True)

        # followedUser serializer.data: [OrderedDict([('id', 3), ('acceptedRequest', True), ('follower', 1), ('followed', 4)])]

        userIdInFollwed = []
        for followedRelation in followedsSerializer.data:
            userIdInFollwed.append(followedRelation["follower"])

        for followingRelation in followingsSerializer.data:
            if followingRelation["followed"] in userIdInFollwed:
                friendIdList.append(followingRelation["followed"])

        print(friendIdList)
        for friendId in friendIdList:

            user = Author.objects.get(id=friendId)
            if not user:
                return Response({"error": "User not found"}, status=404)

            user_id = user.id
            full_name = f"{user.displayName}"
            profileImage = user.profileImage  # Need to solve
            email = user.email
            context = {
                "user_id": user_id,
                "full_name": full_name,
                "profileImage": profileImage,
                "email": email,
            }
            return_package.append(context)
        return Response(return_package)


class RemoteCheckFollow(APIView):
    authentication_classes = [BasicOrTokenAuthentication]

    def get(self, request, author_id, foreign_author_id):
        print("MADE IT HERE!")
        if "/" in author_id:  # Check if author_id is a URL
            author_id = extract_uuid(author_id)  # Extract UUID from URL
        if "/" in foreign_author_id:  # Check if author_id is a URL
            foreign_author_id = extract_uuid(foreign_author_id)  # Extract UUID from URL

        following = Follows.objects.filter(
            followed_id=author_id,
            follower_id=foreign_author_id,
            acceptedRequest=True,
        )

        if not following.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        actor = Author.objects.get(id=author_id)
        actor = AuthorSerializer(actor)
        object = Author.objects.get(id=foreign_author_id)
        object = AuthorSerializer(object)

        response = {
            "type": "Follow",
            "summary": str(actor.data["displayName"])
            + " wants to follow "
            + str(object.data["displayName"]),
            "actor": actor.data,
            "object": object.data,
        }

        return Response(response, status=status.HTTP_200_OK)
