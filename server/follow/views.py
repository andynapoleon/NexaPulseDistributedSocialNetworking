from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from authors.models import Author
from follow.models import Follows
from rest_framework.decorators import api_view
from .serializers import FollowsSerializer


class FollowView(APIView):
    permission_classes = [IsAuthenticated] #[IsAuthenticated]

    def post(self, request, user_id):
        userId1 = user_id
        userId2 = request.data.get('userId2')
        if (userId1 == userId2):
            return Response({'error': 'UserId2 and UserId1 must be unique'}, status=status.HTTP_400_BAD_REQUEST)

        if not (userId2):
            return Response({'error': 'UserId2 must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user1 = self.get_user_from_id(userId1)
        user2 = self.get_user_from_id(userId2)

        if (user1 == user2):
            return Response({'error': 'Two users must be unique'}, status=status.HTTP_400_BAD_REQUEST)

        if not (user1 and user2):
            return Response({'error': 'One or both users not found'}, status=status.HTTP_404_NOT_FOUND)

        # Follow: Create the follow relationship
        follow = Follows(follower=user1, followed=user2)
        follow.save()
        return Response({'success': 'Now following userId2'}, status=status.HTTP_200_OK)

    def delete(self, request,user_id):
        userId1 = user_id
        userId2 = request.data.get('userId2')

        if not (userId1 and userId2):
            return Response({'error': 'UserId2 must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user1 = self.get_user_from_id(userId1)
        user2 = self.get_user_from_id(userId2)

        if not (user1 and user2):
            return Response({'error': 'One or both users not found'}, status=status.HTTP_404_NOT_FOUND)

        # Unfollow: Remove the existing follow relationship
        Follows.objects.filter(follower=user1, followed=user2).delete()
        return Response({'success': 'Unfollowed userId2'}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request, user_id):
        # userId1 is the follower
        userId1 = user_id
        # userId2 is being followed
        target_user_id  = request.query_params.get('userId2')

        if not (target_user_id ):
            return Response({'error': 'UserId2 must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user1 = self.get_user_from_id(userId1)
        user2 = self.get_user_from_id(target_user_id)

        if not (user2):
            return Response({'error': 'One or both users not found'}, status=status.HTTP_404_NOT_FOUND)

        print("follower_id", user1)
        print("followed_id", user2)
        # Check if the follow relationship exists
        follow_exists = Follows.objects.filter(follower_id=user_id, followed_id=target_user_id).exists()

        return Response({'following': follow_exists}, status=status.HTTP_200_OK)

    def get_user_from_id(self, user_id):
        try:
            user = Author.objects.get(id=user_id)
            return user
        except Author.DoesNotExist:
            return None
        
class FollowAllView(APIView):
    permission_classes = [IsAuthenticated] #[IsAuthenticated]

    def get(self, request):
        followers = Follows.objects.all()
        serializer = FollowsSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)