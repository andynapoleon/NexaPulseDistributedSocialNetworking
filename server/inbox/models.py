from django.db import models
from authors.models import Author
from posts.models import Post
from likes.models import PostLikes
from likes.models import CommentLikes
from comments.models import Comment
from follow.models import Follows


# Create your models here.
class Inbox(models.Model):

    authorId = models.OneToOneField(Author, on_delete=models.CASCADE)

    type = models.CharField(max_length=100)

    posts = models.ManyToManyField(Post, blank=True)

    follow_requests = models.ManyToManyField(Follows, blank=True)

    comment_likes = models.ManyToManyField(CommentLikes, blank=True)

    post_likes = models.ManyToManyField(PostLikes, blank=True)

    comments = models.ManyToManyField(Comment, blank=True)
