from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from .models import Author
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
import uuid

class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Author.objects.create(
            displayName="John Doe", github="https://github.com/johndoe", email="johndoe@example.com", is_active=True
        )
        self.valid_user_id = self.user.id
        self.invalid_user_id = uuid.uuid4()  # Non-existent user ID
        
        # Create an instance of Author and authenticate the client
        self.test_author = Author.objects.create(displayName='testuser testuser', github='https://github.com/testuser', email='testuser@example.com', is_active=True)
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

    def test_get_profile(self):
        url = reverse("Profile", args=[self.valid_user_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "full_name": "John Doe",
                "github": "https://github.com/johndoe",
                "email": "johndoe@example.com",
            },
        )


class AuthorAPITestCase(TestCase):
    def setUp(self):
        # Set up test author
        self.client = APIClient()
        self.author = Author.objects.create(email='test@example.com', displayName='Test User', github='testuser', is_active=True)
        print(self.author.id)
        # Create an instance of Author and authenticate the client
        self.test_author = Author.objects.create(displayName='testuser testuser', github='https://github.com/testuser', email='testuser@example.com', is_active=True) 
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        self.invalid_user_id = uuid.uuid4()

        
    def test_create_author(self):
        url = reverse('New author')
        data = {'email': "asc@gmail.com", 'password': "password", 'displayName': "asc", 'github': "https://github.com/", 'id': None, 'isForeign': False}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
    def test_author_list(self):
        url = reverse('Author List')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_specific_author(self):
        # Ensure we can retrieve a specific author
        print(self.author.id)
        url = reverse('Get specific author', kwargs={'author_id': self.author.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['displayName'], 'Test User')

    def test_update_author(self):
        # Test we can update an existing author
        url = reverse('Get specific author', kwargs={'author_id': self.author.id})
        data = {'email': 'updated@example.com', 'displayName': 'Updated name', 'github': 'updatedgithub'}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.author.refresh_from_db()  
        url = reverse('Get specific author', kwargs={'author_id': self.author.id})
        response = self.client.get(url)
        self.assertEqual(response.data['github'], 'updatedgithub')
        self.assertEqual(response.data['displayName'], 'Updated name') 

    def test_non_existing_author(self):
        # Ensure we get a 404 response when trying to retrieve a non-existing author
        url = reverse('Get specific author', kwargs={'author_id': self.invalid_user_id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_bad_request(self):
    #     # Send a PUT request with wrong data
    #     url = reverse('Get specific author', kwargs={'author_id': self.author.id})
    #     data = {'gmail': 'updated@gmail.com'}  # Missing 'displayName'
    #     response = self.client.put(url, data, format='json')

    #     # Ensure the response status code is 400 Bad Request
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
