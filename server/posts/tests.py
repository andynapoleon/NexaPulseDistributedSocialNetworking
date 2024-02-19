from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status

class PostViewsTestCase(TestCase):
    def test_get_posts(self):
        url = reverse('get_posts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)