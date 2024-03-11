from rest_framework.test import APIClient, APITestCase
from .models import Author, Post, Comment
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

class CommentAPITestCase(APITestCase):
    def setUp(self):
        # Set up test author
        self.client = APIClient()
        self.author = Author.objects.create(email='test@example.com', firstName='Test', lastName='User', github='testuser')

        # Create an instance of Author and authenticate the client
        self.test_author = Author.objects.create(firstName='testuser', lastName='testuser', github='https://github.com/testuser', email='testuser@example.com')
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Create a post to be able to comment on it
        self.test_post = Post.objects.create(title='Test Post', content='This is a test post content', authorId=self.author)

        # Create a comment
        self.test_comment = Comment.objects.create(type='comment', content_type='text/plain', comment='This is a test comment', author=self.author, post=self.test_post)
        

    def test_comment_creation(self):
        # Ensure we can create a new comment
        url = reverse('get_post_comments', kwargs={'author_id': self.author.id, 'post_id': self.test_post.id})
        data = {
            'type': 'comment',
            'content_type': 'text/plain',
            'content': 'This is another test comment',
            'author': self.author.id,
            'post': self.test_post.id
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    def test_get_comments(self):
        url = reverse('get_post_comments', kwargs={'author_id': self.author.id, 'post_id': self.test_post.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
