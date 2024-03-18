from rest_framework.test import APIClient, APITestCase
from .models import Author, Post, Comment
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
import uuid

class CommentAPITestCase(APITestCase):
    def setUp(self):
        # Set up test author
        self.client = APIClient()
        self.author = Author.objects.create(email='test@example.com', displayName='Test', github='testuser', is_active=True)

        # Create an instance of Author and authenticate the client
        self.test_author = Author.objects.create(displayName='testuser', github='https://github.com/testuser', email='testuser@example.com', is_active=True)
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Create a post to be able to comment on it
        self.test_post = Post.objects.create(title='Test Post', content='This is a test post content', authorId=self.author)

        # Generate a random UUID
        self.invalid_post_id = str(uuid.uuid4())  

        # Create a comment
        self.comment_data = {
            "postId": self.test_post,
            "author": self.author,
            "content_type": "text",
            "comment": "Test comment content"
        }
        self.comment = Comment.objects.create(**self.comment_data)
        # Create another comment
        self.another_comment_data = {
            "postId": self.test_post,
            "author": self.author,
            "content_type": "text",
            "comment": "Test comment content"
        }
        self.comment = Comment.objects.create(**self.another_comment_data)
        
        
    def test_get_comments(self):
        # Ensure we can get list of comments
        url = reverse('get_post_comments', kwargs={'author_id': self.author.id, 'post_id': self.test_post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_comment_creation(self):
        # Ensure we can create a new comment
        url = reverse('get_post_comments', kwargs={'author_id': self.author.id, 'post_id': self.test_post.id})
        data = {
            'type': 'comment',
            'content_type': 'text/plain',
            'content': 'This is another test comment',
            'author': self.author.id,
            'postId': self.test_post.id
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthorized_post_comment(self):
        # Ensure unauthorized authors cannot comment
        url = reverse("get_post_comments", kwargs={"author_id": self.author.id, "post_id": self.test_post.id})
        unauthorized_comment_data = {
            'type': 'comment',
            'content_type': 'text/plain',
            'content': 'This is another test comment',
            'author': self.test_author.id,
            'postId': self.test_post.id
        }
        response = self.client.post(url, data=unauthorized_comment_data, format='json')
        #print(response.content)  # Print response content for debugging
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_nonexistent_post_comment(self):
        # Ensure nonexistent posts cannot be commented
        url = reverse("get_post_comments", kwargs={"author_id": self.author.id, "post_id": self.invalid_post_id})
        comment_data = {
            'type': 'comment',
            'content_type': 'text/plain',
            'content': 'This is another test comment',
            'author': self.author.id,
            'postId': self.invalid_post_id
        }
        response = self.client.post(url, data=comment_data, format='json')
        # print("HEre",response.content)  # Print response content for debugging
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_not_found(self):
            # Ensure nonexistent comment are handled appropriately
            url = reverse("get_post_comments", kwargs={"author_id": self.author.id, "post_id": self.invalid_post_id})
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_bad_request(self):
    #     url = reverse("get_post_comments", kwargs={"author_id": self.author.id, "post_id": self.test_post.id})
    #     invalid_data = {
    #         'type': 'comment',
    #         'content_type': 'text/plain',
    #         'author': self.author.id,
    #         'postId': self.test_post.id,
    #         'invalidField': 'value'
    #         }
    #     response = self.client.post(url, data=invalid_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    # WE CAN MAKE SO THAT COMMENTS CANNOT BE EMPTY -- Later