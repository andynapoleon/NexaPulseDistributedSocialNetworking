from django.db import models
from authors.models import Author
from posts.models import Post
import uuid

class Comment(models.Model):

    type = models.CharField(max_length=20, default="comment")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    content_type = models.CharField(max_length=50, default="") # Maybe if we have choice od contentType we can make this a ChoiceField

    comment = models.TextField(default="")

    published = models.DateTimeField(auto_now_add=True)
