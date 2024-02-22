from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from authors.models import Author
from follow.models import Follows

class FollowView(APIView):
    permission_classes = [AllowAny] #[IsAuthenticated]

    def post(self, request):
        data = request.data
        userId1 = data.get('userId1')
        userId2 = data.get('userId2')

        if not (userId1 and userId2):
            return Response({'error': 'Both userId1 and userId2 must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user1 = self.get_user_from_id(userId1)
        user2 = self.get_user_from_id(userId2)

        if not (user1 and user2):
            return Response({'error': 'One or both users not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the follow relationship exists
        follow_exists = Follows.objects.filter(follower=user1, followed=user2).exists()

        if follow_exists:
            # Unfollow: Remove the existing follow relationship
            Follows.objects.filter(follower=user1, followed=user2).delete()
            return Response({'success': 'Unfollowed userId2'}, status=status.HTTP_204_NO_CONTENT)
        else:
            # Follow: Create the follow relationship
            follow = Follows(follower=user1, followed=user2)
            follow.save()
            return Response({'success': 'Now following userId2'}, status=status.HTTP_200_OK)

    def delete(self, request):
        data = request.data
        userId1 = data.get('userId1')
        userId2 = data.get('userId2')

        if not (userId1 and userId2):
            return Response({'error': 'Both userId1 and userId2 must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user1 = self.get_user_from_id(userId1)
        user2 = self.get_user_from_id(userId2)

        if not (user1 and user2):
            return Response({'error': 'One or both users not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the follow relationship exists
        follow_exists = Follows.objects.filter(follower=user1, followed=user2).exists()

        if follow_exists:
            # Unfollow: Remove the existing follow relationship
            Follows.objects.filter(follower=user1, followed=user2).delete()
            return Response({'success': 'Unfollowed userId2'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Follow relationship does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        userId1 = request.query_params.get('userId1')
        userId2 = request.query_params.get('userId2')

        if not (userId1 and userId2):
            return Response({'error': 'Both userId1 and userId2 must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        user1 = self.get_user_from_id(userId1)
        user2 = self.get_user_from_id(userId2)

        if not (user1 and user2):
            return Response({'error': 'One or both users not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the follow relationship exists
        follow_exists = Follows.objects.filter(follower=user1, followed=user2).exists()

        if follow_exists:
            return Response({'following': True}, status=status.HTTP_200_OK)
        else:
            return Response({'following': False}, status=status.HTTP_200_OK)

    def get_user_from_id(self, user_id):
        try:
            user = Author.objects.get(id=user_id)
            return user
        except Author.DoesNotExist:
            return None