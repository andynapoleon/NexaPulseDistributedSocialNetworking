from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status

class PostViewsTestCase(TestCase):
    def test_get_post(self):
        # Replace 'author_id' and 'post_id' with valid IDs for testing
        author_id = 'valid_author_id'
        post_id = 'valid_post_id'

        # Reverse the 'get_post' URL pattern with the author ID and post ID
        url = reverse('get_post', kwargs={'author_id': author_id, 'post_id': post_id})
        
        # Make a GET request to retrieve the specific post
        response = self.client.get(url)

        # Assert that the response status code is HTTP_200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)