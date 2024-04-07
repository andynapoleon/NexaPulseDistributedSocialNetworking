from django.db import models

# Create your models here.
from authors.models import Author
import uuid
from datetime import datetime


class Post(models.Model):

    type = models.CharField(default="post", max_length=4, editable=False)

    VISIBILITY_CHOICES = [
        ("PUBLIC", "Public"),
        ("FRIENDS", "Friends"),
        ("UNLISTED", "Unlisted"),
    ]

    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default=("PUBLIC", "Public")
    )
    # for visibility PUBLIC means it is open to the wild web
    # FRIENDS means if we're friends I can see the post
    # FRIENDS should've already been sent the post so they don't need this

    # id of the post
    id = models.CharField(primary_key=True, default=uuid.uuid4, max_length=128, editable=False)

    authorId = models.ForeignKey(Author, on_delete=models.CASCADE)

    comments = models.ForeignKey(
        "comments.Comment", on_delete=models.CASCADE, null=True, blank=True
    )

    # title of a post
    title = models.CharField(max_length=255, default="")

    published = models.DateTimeField(auto_now_add=True)

    source = models.CharField(max_length=255, default="", null=True, blank=True)

    description = models.CharField(max_length=255, default="", null=True, blank=True)

    # The content type of the post assume either
    # text/markdown -- common mark
    # text/plain -- UTF-8
    # application/base64
    # image/png;base64 # this is an embedded png
    # -- images are POSTS. So you might have a
    # user make 2 posts if a post includes an image!
    # image/jpeg;base64 # this is an embedded jpeg
    CONTENT_CHOICES = [
        ("text/plain", "plain"),
        ("text/markdown", "markdown"),
        ("image/png;base64", "png"),
        ("image/jpeg;base64", "jpeg"),
    ]
    contentType = models.CharField(
        max_length=20, choices=CONTENT_CHOICES, default="text/plain"
    )
    content = models.TextField(default="")
    originalContent = models.TextField(default="")

    image_ref = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True
    )

    sharedBy = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    sharedBy = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="shared_posts"
    )
    isShared = models.BooleanField(default=False)
