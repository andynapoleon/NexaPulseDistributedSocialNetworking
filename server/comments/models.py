from django.db import models
from authors.models import Authors
from posts.models import Post
# Create your models here.

class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    content = models.TextField()
