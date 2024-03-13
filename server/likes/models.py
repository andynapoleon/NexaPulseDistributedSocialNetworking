from django.db import models
from authors.models import Author
from posts.models import Post
from comments.models import Comment

# Create your models here.
class PostLikes(models.Model):

    summary = models.CharField(max_length=50, default="", editable=False)

    type = models.CharField(max_length=20, default="Like", editable=False)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    object = models.CharField(max_length=50, default="", editable=False)

    class Meta:
        # prevents dublicate likes
        unique_together = ('author', 'post')

class CommentLikes(models.Model):
    
    summary = models.CharField(max_length=50, default="", editable=False)

    type = models.CharField(max_length=20, default="Like", editable=False)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    object = models.CharField(max_length=50, default="", editable=False)

    class Meta:
        # prevents dublicate likes
        unique_together = ('author', 'post', 'comment')