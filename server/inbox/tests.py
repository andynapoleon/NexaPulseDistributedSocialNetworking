# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken
from authors.models import Author
from .models import Inbox

class InboxViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test authors
        self.author1 = Author.objects.create(displayName='John', email='Doe@gmail.com',is_active=True)
        self.author2 = Author.objects.create(displayName='Jane', email='Joe@gmail.com',is_active=True)
        
        # Create test inbox for author1
        self.inbox_author1 = Inbox.objects.create(authorId=self.author1)
        
        # Set up authentication headers
        self.token = AccessToken.for_user(self.author1)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

    def test_get_inbox(self):
        url = reverse('inbox', kwargs={'author_id': self.author1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_to_inbox(self):
        url = reverse('inbox', kwargs={'author_id': self.author1.id})
        data = {
            'type': 'post',
            'id': 1,  # Assuming postId exists
            'authorId': self.author2.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add additional assertions as needed

    def test_follow_request(self):
        url = reverse('inbox', kwargs={'author_id': self.author1.id})
        data = {
            'type': 'follow',
            'userId1': self.author2.id,  # Assuming userId1 is follower
            'userId2': self.author1.id,  # Assuming userId2 is followed
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add additional assertions as needed

    def test_delete_inbox(self):
        url = reverse('inbox', kwargs={'author_id': self.author1.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
