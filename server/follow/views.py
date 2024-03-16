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


class FollowView(APIView):
    permission_classes = [IsAuthenticated]  # [IsAuthenticated]

    def put(self, request, user_id):
        userId1 = request.data.get("userId1")
        userId2 = request.data.get("userId2")
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
            return Response(
                {"success": "Follow request accepted"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Request does not exist"}, status=status.HTTP_400_BAD_REQUEST
            )

    def post(self, request, user_id):
        sender_host = request.data.get("senderHost")
        receiver_host = request.data.get("receiverHost")[0:-1]
        print(sender_host)
        print(receiver_host)
        # local
        if sender_host == receiver_host:
            print("LOCAL")
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
        # remote
        else:
            print("REMOTE")
            userId2 = request.data.get("userId2")
            node = Node.objects.filter(host=receiver_host)
            request_url = f"{node.host}/service/authors{userId2}/inbox/"
            try:
                response = requests.post(
                    request_url, json=request.data, auth=(node.username, node.password)
                )
                print("status code response", response.status_code)
                if response.status_code == 200:
                    print("Succeeded sening friend requests")
                    return Response(
                        {"success": "Now following userId2"}, status=status.HTTP_200_OK
                    )
            except requests.exceptions.RequestException as e:
                print(f"couldnt sent friend request to remote inbox: {e}")
                return Response(
                    {"error": f"Couldnt sent friend request to remote inbox: {e}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

    def delete(self, request, user_id):
        # target_user_id is being followed
        user_being_follow_id = request.query_params.get("userId2")
        print("user_being_follow_id:", user_being_follow_id)

        if not (user_being_follow_id):
            return Response(
                {"error": "UserId2 must be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Follows.objects.filter(
            followed_id=user_being_follow_id, follower_id=user_id
        ).delete()
        return Response(
            {"success": "Unfollowed userId2"}, status=status.HTTP_204_NO_CONTENT
        )

    def get(self, request, user_id):
        # userId2 is being followed
        print(user_id)
        target_user_id = request.query_params.get("userId2")
        print(target_user_id)

        if not (target_user_id):
            return Response(
                {"error": "UserId2 must be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user1 = Author.objects.get(id=user_id)
        user2 = Author.objects.get(id=target_user_id)  # NOT WORKING!!!

        # Check if the follow relationship exists
        ####
        requestObj = Follows.objects.filter(followed=user1, follower=user2).first()

        if requestObj:
            follow_exists = True
            accepted_request = (
                requestObj.acceptedRequest
            )  # Assuming acceptedRequest is a field of the Follows model
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
            profileImageUrl = user.profileImage  # Need to solve
            email = user.email
            context = {
                "user_id": user_id,
                "full_name": full_name,
                "profileImageUrl": "https://seeded-session-images.scdn.co/v2/img/122/secondary/artist/4tmoBDLDleElXopuhDljGR/en",
                "email": email,
            }
            return_package.append(context)
        return Response(return_package)


class UserFollowedView(APIView):
    permission_classes = [IsAuthenticated]  # [IsAuthenticated]

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
            profileImageUrl = user.profileImage  # Need to solve
            email = user.email
            context = {
                "user_id": user_id,
                "full_name": full_name,
                "profileImageUrl": "https://seeded-session-images.scdn.co/v2/img/122/secondary/artist/4tmoBDLDleElXopuhDljGR/en",
                "email": email,
            }
            return_package.append(context)
        return Response(return_package)


class UserFriendsView(APIView):
    permission_classes = [IsAuthenticated]  # [IsAuthenticated]

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
            profileImageUrl = user.profileImage  # Need to solve
            email = user.email
            context = {
                "user_id": user_id,
                "full_name": full_name,
                "profileImageUrl": "https://seeded-session-images.scdn.co/v2/img/122/secondary/artist/4tmoBDLDleElXopuhDljGR/en",
                "email": email,
            }
            return_package.append(context)
        return Response(return_package)
