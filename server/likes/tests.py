from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken
from .models import PostLikes, CommentLikes, Author, Post, Comment

class LikesAPITest(TransactionTestCase):
    def setUp(self):
        # Set up test author
        self.client = APIClient()
        self.author = Author.objects.create(email='test@example.com', displayName='Test', github='testuser', is_active=True)

        # Create an instance of Author and authenticate the client
        self.test_author = Author.objects.create(displayName='testuser', github='https://github.com/testuser', email='testuser@example.com', is_active=True)
        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))

        # Create a post to be able to like on it
        self.test_post = Post.objects.create(title='Test Post', content='This is a test post content', authorId=self.author)
        
        # Create a comment to be able to like on it
        self.comment = Comment.objects.create(author=self.author, postId=self.test_post, comment="Test comment")


    def test_get_post_likes(self):
        # Ensure list of like shows likes of other authors
        like1 = PostLikes.objects.create(author=self.author, post=self.test_post) # by other authors
        like2 = PostLikes.objects.create(author=self.test_author, post=self.test_post) # by main author itself
        url = reverse('get_post_likes', kwargs={'author_id': self.test_author.id, 'post_id': self.test_post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_all_likes_in_post(self):
        # Ensure a list of likes to show likes from all authors
        like1 = PostLikes.objects.create(author=self.author, post=self.test_post) # by other authors
        like2 = PostLikes.objects.create(author=self.test_author, post=self.test_post) # by main author itself
        url = reverse('get_list_of_likes', kwargs={'author_id': self.test_author.id, 'post_id': self.test_post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_comment_likes(self):
        # Ensure list of like shows likes of other authors
        like1 = CommentLikes.objects.create(author=self.author, post=self.test_post, comment=self.comment)
        like2 = CommentLikes.objects.create(author=self.test_author, post=self.test_post, comment=self.comment)
        url = reverse('get_comment_likes', kwargs={'author_id': self.test_author.id, 'post_id': self.test_post.id, 'comment_id': self.comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


    def test_like_post(self):
        # Ensure post can be liked
        url = reverse('like_unlike_post', kwargs={'author_id': self.author.id})
        data = {'author': self.author.id, 'post': self.test_post.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PostLikes.objects.filter(author=self.author, post=self.test_post).exists())

    def test_unlike_post(self):
        # Ensure post can be unliked
        like = PostLikes.objects.create(author=self.author, post=self.test_post)
        url = reverse('like_unlike_post', kwargs={'author_id': self.author.id})
        data = {'author': self.author.id, 'post': self.test_post.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PostLikes.objects.filter(author=self.author, post=self.test_post).exists())

    def test_like_comment(self):
        # Ensure comments can be liked
        url = reverse('like_unlike_comment', kwargs={'author_id': self.author.id})
        data = {'author': self.author.id, 'post': self.test_post.id, 'comment': self.comment.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CommentLikes.objects.filter(author=self.author, post=self.test_post, comment=self.comment).exists())

    def test_unlike_comment(self):
        # Ensure comments can be unliked
        like = CommentLikes.objects.create(author=self.author, post=self.test_post, comment=self.comment)
        url = reverse('like_unlike_comment', kwargs={'author_id': self.author.id})
        data = {'author': self.author.id, 'post': self.test_post.id, 'comment': self.comment.id}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CommentLikes.objects.filter(author=self.author, post=self.test_post, comment=self.comment).exists())

    def test_duplicate_like_post(self):
        # Ensure no duplicate likes is possible
        like = PostLikes.objects.create(author=self.author, post=self.test_post)
        url = reverse('like_unlike_post', kwargs={'author_id': self.author.id})
        data = {'author': self.author.id, 'post': self.test_post.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("unique constraint failed", response.data["error"].lower())
        self.assertEqual(PostLikes.objects.filter(author=self.author, post=self.test_post).count(), 1)

    def test_like_post_on_behalf_of_other(self):
        # Ensure likes cannot be posted on belaf of other users
        other_author = Author.objects.create(displayName="other_author", email="other_author@test.com", github='https://github.com/testuser', is_active=True)
        url = reverse('like_unlike_post', kwargs={'author_id': self.author.id})
        data = {'author': other_author.id, 'post': self.test_post.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("not authorized", response.data["error"].lower())
        self.assertFalse(PostLikes.objects.filter(author=other_author, post=self.test_post).exists())