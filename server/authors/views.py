from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Author
from .serializers import AuthorSerializer


class AuthorList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return AuthorSerializer

    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            serializer = AuthorSerializer(author, data=request.data, partial=True)
            print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Profile(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_from_id(self, user_id):
        try:
            user = Author.objects.get(id=user_id)
            return user
        except Author.DoesNotExist:
            return None

    def get(self, request, user_id):
        user = self.get_user_from_id(user_id)
        if not user:
            return Response({"error": "User not found"}, status=404)

        full_name = f"{user.firstName} {user.lastName}"
        github = user.github
        email = user.email
        context = {
            "full_name": full_name,
            "github": github,
            "email": email,
        }
        return Response(context)

    def put(self, request, user_id):
        # if not request.user.is_authenticated:
        #     return Response(
        #         {"error": "Authentication credentials were not provided."},
        #         status=status.HTTP_401_UNAUTHORIZED,
        #     )
        if request.user.id != user_id:
            return Response(
                {"error": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user = self.get_user_from_id(user_id)
        if not user:
            return Response({"error": "User not found"}, status=404)

        # Assuming the request contains data to update the user profile
        # Extract the data from request.data and update the user object
        full_name = request.data.get("name", "")
        github = request.data.get("github", "")
        email = request.data.get("email", "")

        # Update user object
        user.firstName, user.lastName = (
            full_name.split()
        )  # Split full name into first and last name
        user.github = github
        user.email = email
        user.save()

        # Return updated user data
        updated_data = {
            "full_name": full_name,
            "github": github,
            "email": email,
        }
        return Response(updated_data)
