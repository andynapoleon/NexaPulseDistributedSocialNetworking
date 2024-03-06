from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Follows, Author
from .serializers import FollowsSerializer

# Test user data
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpassword"

TEST_USER_EMAIL_2 = "test2@example.com"
TEST_USER_PASSWORD_2 = "testpassword2"

class FollowViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.author1 = Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        self.author2 = Author.objects.TEST_USER_EMAIL_2(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD_2,
        )
    def test_put_follow_request_accepted(self):
        Follows.objects.create(follower=self.author1, followed=self.author2)
        response = self.client.put(f'/api/follow/{self.user1.id}/', {'userId1': self.user1.id, 'userId2': self.user2.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class FollowAllViewTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.author1 = Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        self.author2 = Author.objects.TEST_USER_EMAIL_2(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD_2,
        )
    def test_get_followers_list(self):
        Follows.objects.create(follower=self.author1, followed=self.author2)
        response = self.client.get(f'/api/follow/all/{self.user2.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class UserFollowingViewTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.author1 = Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        self.author2 = Author.objects.TEST_USER_EMAIL_2(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD_2,
        )
    def test_get_user_following_list(self):
        Follows.objects.create(follower=self.author1, followed=self.author2, acceptedRequest=True)
        response = self.client.get(f'/api/user/{self.user1.id}/following/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserFollowedViewTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.author1 = Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        self.author2 = Author.objects.TEST_USER_EMAIL_2(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD_2,
        )
    def test_get_user_followed_list(self):
        Follows.objects.create(follower=self.author2, followed=self.author1, acceptedRequest=True)
        response = self.client.get(f'/api/user/{self.user1.id}/followed/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserFriendsViewTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.author1 = Author.objects.create_user(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD,
        )
        self.author2 = Author.objects.TEST_USER_EMAIL_2(
            email=TEST_USER_EMAIL,
            password=TEST_USER_PASSWORD_2,
        )
    def test_get_user_friends_list(self):
        Follows.objects.create(follower=self.author1, followed=self.author2, acceptedRequest=True)
        Follows.objects.create(follower=self.author2, followed=self.author1, acceptedRequest=True)
        response = self.client.get(f'/api/user/{self.user1.id}/friends/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

