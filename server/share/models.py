from django.db import models

# Create your models here.
from authors.models import Author
from posts.models import Post


class SharedPost(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("author", "post")
