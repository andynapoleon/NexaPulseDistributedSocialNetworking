from rest_framework.test import APIClient, APITestCase
from .models import Author
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Author.objects.create(
            firstName="John", lastName="Doe", github="https://github.com/johndoe", email="johndoe@example.com"
        )
        self.valid_user_id = self.user.id
        self.invalid_user_id = self.valid_user_id + 1  # Non-existent user ID
        
        # Create an instance of Author and authenticate the client
        self.test_author = Author.objects.create(firstName='testuser', lastName='testuser', github='https://github.com/testuser', email='testuser@example.com')
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

    # Other test cases go here
