from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient
from rest_framework import status
from authors.models import Author, CustomUserManager
from auth.views import LoginView, TokenRefreshAPIView

# Test user data
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword"
TEST_USER_NAME = "John Doe"
TEST_USER_GITHUB = "johndoe"


class LoginViewTests(TestCase):
    def setUp(self):
        # Create a test user
        Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )

    def test_login_success(self):
        """
        Test successful login with valid credentials.
        """
        client = APIClient()
        data = {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
        response = client.post("/api/login/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)
        self.assertEqual(response.data["email"], TEST_USER_EMAIL)
        self.assertEqual(response.data["name"], f"{TEST_USER_NAME}")
        self.assertEqual(response.data["github"], TEST_USER_GITHUB)
        self.assertEqual(response.data["id"], 1)  # Assuming user ID starts from 1

    def test_login_invalid_credentials(self):
        """
        Test login failure with invalid credentials.
        """
        client = APIClient()
        data = {"email": TEST_USER_EMAIL, "password": "invalid_password"}
        response = client.post("/api/login/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid Credentials")

    def test_login_missing_fields(self):
        """
        Test login failure with missing email or password fields.
        """
        client = APIClient()
        # Missing email
        data = {"password": TEST_USER_PASSWORD}
        response = client.post("/api/login/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Missing password
        data = {"email": TEST_USER_EMAIL}
        response = client.post("/api/login/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenRefreshViewTests(TestCase):
    def setUp(self):
        # Create a test user and get a refresh token
        user = Author.objects.create_user(
            email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD
        )
        refresh = RefreshToken.for_user(user)
        self.refresh_token = str(refresh)

    def test_refresh_success(self):
        """
        Test successful token refresh with a valid refresh token.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.refresh_token}")
        data = {"refresh_token": self.refresh_token}
        response = client.post("/api/token/refresh/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_refresh_invalid_token(self):
        """
        Test token refresh failure with an invalid refresh token.
        """
        client = APIClient()
        # Send invalid token
        data = {"refresh_token": "invalid_token"}
        response = client.post("/api/token/refresh/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid refresh token")

    def test_refresh_missing_token(self):
        """
        Test token refresh failure with missing refresh token in request body.
        """
        client = APIClient()
        # No data sent in the request body
        response = client.post("/api/token/refresh/", format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
