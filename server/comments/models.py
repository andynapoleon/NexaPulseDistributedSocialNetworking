from django.db import models
from authors.models import Author
from posts.models import Post
# Create your models here.

class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
