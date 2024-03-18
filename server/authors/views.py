from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Author
from .serializers import AuthorSerializer
from auth.BasicOrTokenAuthentication import BasicOrTokenAuthentication
from SocialDistribution.settings import SERVER
from rest_framework import generics


class AuthorList(generics.ListCreateAPIView):
    serializer_class = (
        AuthorSerializer  # Assuming AuthorSerializer is your serializer class
    )
    authentication_classes = [
        BasicOrTokenAuthentication
    ]  # Apply BasicAuthentication only for AuthorList view

    def get_queryset(self):
        return Author.objects.all().filter(host=SERVER)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data_with_type = serializer.data
        for item in data_with_type:
            item["type"] = "author"
            item.pop("password", None)

        response = {
            "type": "authors",
            "items": data_with_type,
        }

        return Response(response, status=status.HTTP_200_OK)


class AuthorDetail(generics.RetrieveAPIView):
    authentication_classes = [BasicOrTokenAuthentication]

    def get_serializer_class(self):
        return AuthorSerializer

    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            serializer = AuthorSerializer(author)
            response = serializer.data
            return Response(response, status=200)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            serializer = AuthorSerializer(author, data=request.data, partial=True)
            # print(serializer.is_valid())
            if serializer.is_valid():
                serializer.save()
                response = serializer.data
                return Response(response, status=200)
            return Response(serializer.errors, status=400)
        except Author.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class AuthorCreate(APIView):
    permission_classes = [AllowAny]

    # create a new author manually
    def post(self, request):
        data = request.data
        try:
            author = Author.objects.get(email=data["email"])
            return Response(
                {"error": "User with this email already exists"}, status=400
            )
        except Author.DoesNotExist:
            if data["id"] == None:
                new_author = Author.objects.create_user(
                    email=data["email"],
                    password=data["password"],
                    displayName=data["displayName"],
                    profileImage=data["profileImage"],
                    github=data["github"],
                    isForeign=data["isForeign"],
                )
            else:
                new_author = Author.objects.create_user(
                    id=data["id"],
                    host=data["host"],
                    isForeign=data["isForeign"],
                    email=data["email"],
                    password=data["password"],
                    displayName=data["displayName"],
                    profileImage=data["profileImage"],
                    github=data["github"],
                )
            new_author.save()
            serializer = AuthorSerializer(new_author)
            response = serializer.data
            return Response(response, status=201)


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

        full_name = user.displayName
        github = user.github
        email = user.email
        profileImage = user.profileImage
        context = {
            "full_name": full_name,
            "github": github,
            "email": email,
            "profileImage": profileImage,
        }
        return Response(context)

    def put(self, request, user_id):
        # if not request.user.is_authenticated:
        #     return Response(
        #         {"error": "Authentication credentials were not provided."},
        #         status=status.HTTP_401_UNAUTHORIZED,
        #     )
        # if str(request.user.id) != str(user_id):
        #     return Response(
        #         {"error": "You do not have permission to perform this action."},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )

        user = self.get_user_from_id(user_id)
        if not user:
            return Response({"error": "User not found"}, status=404)

        # Assuming the request contains data to update the user profile
        # Extract the data from request.data and update the user object
        full_name = request.data.get("name", "")
        github = request.data.get("github", "")
        email = request.data.get("email", "")
        profileImage = request.data.get("profileImage", "")

        user.displayName = full_name
        user.github = github
        user.email = email
        user.profileImage = profileImage
        user.save()

        # Return updated user data
        updated_data = {
            "full_name": full_name,
            "github": github,
            "email": email,
            "profileImage": profileImage,
        }
        return Response(updated_data)
