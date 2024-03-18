from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from .models import Node
from rest_framework_simplejwt.tokens import AccessToken
from authors.models import Author

class NodeListGetTest(APITestCase):
    def setUp(self):

        # Create some sample active nodes
        self.active_node1 = Node.objects.create(
            host="http://example1.com",
            username="user1",
            password="password1",
            team=1,
            isActive=True
        )
        self.active_node2 = Node.objects.create(
            host="http://example2.com",
            username="user2",
            password="password2",
            team=2,
            isActive=True
        )

        # Create some inactive nodes
        self.inactive_node1 = Node.objects.create(
            host="http://example3.com",
            username="user3",
            password="password3",
            team=3,
            isActive=False
        )
        self.inactive_node2 = Node.objects.create(
            host="http://example4.com",
            username="user4",
            password="password4",
            team=4,
            isActive=False
        )

        self.client = APIClient()

        # Create a JWT token for an active node
        self.test_author = Author.objects.create(displayName='testuser testuser', github='https://github.com/testuser', email='testuser@example.com', is_active=True)
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

    def test_get_active_nodes(self):
        # Send a GET request to the NodeList endpoint
        response = self.client.get(reverse('node-list'))

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the response contains only active nodes
        self.assertEqual(len(response.data['items']), 2)

        # Check that each item in the response is an active node
        for node_data in response.data['items']:
            host = node_data['host']
            node = Node.objects.get(host=host)
            self.assertTrue(node.isActive)
