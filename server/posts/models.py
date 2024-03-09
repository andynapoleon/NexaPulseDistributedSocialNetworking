from django.db import models

# Create your models here.
from authors.models import Author


class Post(models.Model):

    type = models.CharField(max_length=20, default="post")

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
    id = models.AutoField(primary_key=True)
    authorId = models.ForeignKey(Author, on_delete=models.CASCADE)

    # title of a post
    title = models.CharField(max_length=255, default="")

    # ISO 8601 TIMESTAMP
    published = models.DateTimeField(auto_now_add=True)

    # The content type of the post assume either
    # text/markdown -- common mark
    # text/plain -- UTF-8
    # application/base64
    # image/png;base64 # this is an embedded png
    # -- images are POSTS. So you might have a
    # user make 2 posts if a post includes an image!
    # image/jpeg;base64 # this is an embedded jpeg
    content_type = models.CharField(max_length=50, default="")
    content = models.TextField(default="")

    image_ref = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    sharedBy = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True
    )

    # total number of comments for this post
    # count = models.IntegerField(default=0)

    # the first page of comments
    # comments = models.CharField(max_length=255, default="")

    sharedBy = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="shared_posts"
    )
    isShared = models.BooleanField(default=False)

    # OPTIONAL
    # commentsSrc is OPTIONAL and can be missing
    # You should return ~ 5 comments per post.
    # should be sorted newest(first) to oldest(last)
    # this is to reduce API call counts
    # "commentsSrc":{
    #     "type":"comments",
    #     "page":1,
    #     "size":5,
    #       ...
