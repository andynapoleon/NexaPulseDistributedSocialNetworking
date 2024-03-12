from rest_framework.test import APIClient, APITestCase
from .models import Author
from .models import Post
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from authors.serializers import AuthorSerializer


class PostViewsTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create an instance of Author and authenticate the client
        self.test_author = Author.objects.create(
            firstName="testuser",
            lastName="testus er",
            github="https://github.com/testuser",
            email="testuser@example.com",
        )

        self.token = AccessToken.for_user(self.test_author)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.token))

        # Create test posts
        self.public_post = Post.objects.create(
            type="post",
            visibility=Post.VISIBILITY_CHOICES[0][0],  # Public Post
            authorId=self.test_author,
            title="Public Test Post",
            contentType="text/markdown",
            content="This is a test post content.",
        )

        self.friends_post = Post.objects.create(
            type="post",
            visibility=Post.VISIBILITY_CHOICES[1][0],  # Friends Post
            authorId=self.test_author,
            title="Friend Test Post",
            contentType="text/plain",
            content="This is a test post content.",
        )

        self.unlisted_post = Post.objects.create(
            type="post",
            visibility=Post.VISIBILITY_CHOICES[2][0],  # Unlisted Post
            authorId=self.test_author,
            title="Unlisted Test Post",
            contentType="text/plain",
            content="This is a test post content.",
        )

        self.image_post = Post.objects.create(
            type="post",
            visibility=Post.VISIBILITY_CHOICES[0][0],
            authorId=self.test_author,
            title="Image Post",
            contentType="image/jpeg;base64",
            content="old_image_encoded_base64"
        )

        self.post_with_image = Post.objects.create(
            type="post",
            visibility=Post.VISIBILITY_CHOICES[0][0],  # Public Post
            authorId=self.test_author,
            title="Public Test Post",
            contentType="text/plain",
            content="This is a test post content.",
            image_ref=self.image_post,
        )


    def test_getPostList_validAuthorId_returns200status(self):
        url = reverse('post_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_putPublicPost_validAuthorIdAndPostIdContainsImage_returns200status(self):
        url = reverse(
            "image_post_detail",
            args=(self.public_post.authorId.id, self.public_post.id),
        )
        data = {
            "type": "post",
            "visibility": Post.VISIBILITY_CHOICES[0][0],  # Unlisted Post
            "authorId": AuthorSerializer(self.test_author),
            "title": "Updated Image Public Test Post",
            "contentType": "text/markdown",
            "content": "This is a test post content.",
            "image": 'image/png;base64, new_updated_base64_put',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_putPost_validAuthorIdAndPostId_returns200status(self):
        url = reverse(
            "post_detail",
            args=(self.public_post.authorId.id, self.public_post.id),
        )
        data = {
            "type": "post",
            "visibility": Post.VISIBILITY_CHOICES[0][0],
            "authorId": AuthorSerializer(self.public_post.authorId.id),
            'title': 'Updated Title',
            "contentType": "text/markdown",
            'content': 'Updated content of the post.',
            'image': '',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_createPost_validAuthorIdAndPostId_returns200status(self):
        url = reverse(
            "get_author_posts/create_post", 
            args=(self.test_author.id,)
        )
        data = {
            "type": "post",
            "visibility": Post.VISIBILITY_CHOICES[0][0],  # Public Post
            "authorId": self.test_author.id,
            "title": "New Test Post",
            "contentType": "text/markdown",
            "content": "This is a new test post content.",
            "image": '',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            
    # def test_createPost_validAuthorIdAndPostIdContainsImage_returns200status(self):
    #     url = reverse(
    #         "get_author_posts/create_post", 
    #         args=(self.test_author.id,)
    #     )
    #     data = {
    #         "type": "post",
    #         "visibility": Post.VISIBILITY_CHOICES[0][0],  # Public Post
    #         "authorId": self.test_author.id,
    #         "title": "New Test Post",
    #         "contentType": "text/plain",
    #         "content": "This is a new test post content.",
    #         "image": 'image/png:base64, asdfkjl',
    #     }
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_getPost_validAuthorIdAndPostIdContainsImage_returns200status(self):
        url = reverse(
            "image_post",
            args=(self.test_author.id, self.post_with_image.id)
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_putPost_validAuthorIdAndPostIdContainsImage_returns200status(self):
    #     url = reverse(
    #         "post_detail",
    #         args=(self.public_post.authorId.id, self.post_with_image.id),
    #     )
    #     data = {
    #         "type": "post",
    #         "visibility": Post.VISIBILITY_CHOICES[0][0],
    #         "authorId": AuthorSerializer(self.test_author),
    #         'title': 'Updated Title',
    #         "contentType": "text/markdown",
    #         'content': 'Updated content of the post.',
    #         'image': 'image/png;base64, NEWIMAGE',
    #     }
    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)




    # Integration Tests
    # Named this way: Action, method call, condition, return
    # def getPublicPost_validAuthorIdAndPostId_returns200status(self):
    #     url = reverse('get_post/', args=[self.test_author.id, self.test_post.id])
    #     pass

    # def getPost_invalidAuthorIdAndPostId_returns401status(self):
    #     pass

    # def deletePost_validAuthorIdAndPostId_returns200status(self):
    #     pass

    # def deletePost_invalidAuthorIdAndPostId_returns401status(self):
    #     pass



    # def putPost_invalidAuthorIdAndPostId_returns401status(self):
    #     pass

    

    # def createPost_invalidAuthorIdAndPostId_returns401status(self):
    #     pass

    # def test_retrieve_post(self):
    #     url = reverse('get_post/update_post/delete_post', args=[self.test_author.id, self.test_post.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_update_post(self):
    #     url = reverse('get_post/update_post/delete_post', args=[self.test_author.id, self.test_post.id])
    #     data = {'title': 'Updated Title', 'content': 'Updated content of the post.'}
    #     response = self.client.put(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_post(self):
    #     url = reverse('get_post/update_post/delete_post', args=[self.test_author.id, self.test_post.id])
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_create_post(self):
    #     url = reverse('get_author_posts/create_post', args=[self.test_author.id])
    #     data = {'title': 'New Post', 'content': 'Content of the new post.'}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_retrieve_author_posts(self):
    #     url = reverse('get_author_posts/create_post', args=[self.test_author.id])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
