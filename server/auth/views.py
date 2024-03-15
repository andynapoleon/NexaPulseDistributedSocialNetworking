from django.shortcuts import render

# Create your views here.
from authors.models import Author
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        print(email)
        print(password)
        user = Author.objects.filter(email=email).first()
        if user and user.check_password(password) and user.is_active:
            refresh = RefreshToken.for_user(user)
            token_string = refresh.access_token.__str__()
            refresh_string = str(refresh)
            # print(token_string)
            return Response(
                {
                    "refresh": refresh_string,
                    "access": token_string,
                    "email": email,
                    "name": user.displayName,
                    "github": user.github,
                    "id": user.id,
                    "is_active": user.is_active,
                }
            )
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class TokenRefreshAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Attempt to validate the refresh token
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            # Return the new access token
            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )
