from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Follows, Author
from .serializers import FollowsSerializer
from rest_framework_simplejwt.tokens import AccessToken

# Test user data
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword"

TEST_USER_EMAIL_2 = "test2@example.com"
TEST_USER_PASSWORD_2 = "testpassword2"

class FollowViewTestCase(TestCase):
    def setUp(self):
        # Create an instance of Author and authenticate the client
        self.client = APIClient()
        self.test_author = Author.objects.create(displayName='testuser testuser', github='https://github.com/testuser', email='testuser@example.com', is_active=True)
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Create test users
        self.author1 = Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        self.author2 = Author.objects.create_user(
            email=TEST_USER_EMAIL_2,
            password=TEST_USER_PASSWORD_2,
        )
    def test_put_follow_request_accepted(self):
        Follows.objects.create(follower=self.author1, followed=self.author2)
        response = self.client.put(f'/api/follow/{self.author1.id}', {'userId1': self.author1.id, 'userId2': self.author2.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class FollowAllViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_author = Author.objects.create(displayName='testuser testuser', github='https://github.com/testuser', email='testuser@example.com', is_active=True)
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Create test users
        self.author1 = Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        self.author2 = Author.objects.create_user(
            email=TEST_USER_EMAIL_2,
            password=TEST_USER_PASSWORD_2,
        )
    def test_get_followers_list(self):
        Follows.objects.create(follower=self.author1, followed=self.author2)
        response = self.client.get(f'/api/follow/all/{self.author2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class UserFollowingViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_author = Author.objects.create(displayName='testuser testuser', github='https://github.com/testuser', email='testuser@example.com', is_active=True)
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Create test users
        self.author1 = Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        self.author2 = Author.objects.create_user(
            email=TEST_USER_EMAIL_2,
            password=TEST_USER_PASSWORD_2,
        )
    def test_get_user_following_list(self):
        Follows.objects.create(follower=self.author1, followed=self.author2, acceptedRequest=True)
        response = self.client.get(f'/api/friends/following/{self.author1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserFollowedViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_author = Author.objects.create(displayName='testuser testuser', github='https://github.com/testuser', email='testuser@example.com', is_active=True)
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Create test users
        self.author1 = Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        self.author2 = Author.objects.create_user(
            email=TEST_USER_EMAIL_2,
            password=TEST_USER_PASSWORD_2,
        )
    def test_get_user_followed_list(self):
        Follows.objects.create(follower=self.author2, followed=self.author1, acceptedRequest=True)
        response = self.client.get(f'/api/friends/followed/{self.author1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserFriendsViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_author = Author.objects.create(displayName='testuser testuser', github='https://github.com/testuser', email='testuser@example.com', is_active=True)
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Create test users
        self.author1 = Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        self.author2 = Author.objects.create_user(
            email=TEST_USER_EMAIL_2,
            password=TEST_USER_PASSWORD_2,
        )
    def test_get_user_friends_list(self):
        Follows.objects.create(follower=self.author1, followed=self.author2, acceptedRequest=True)
        Follows.objects.create(follower=self.author2, followed=self.author1, acceptedRequest=True)
        response = self.client.get(f'/api/friends/friends/{self.author1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

