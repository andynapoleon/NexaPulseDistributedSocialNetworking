from django.db import models

# Create your models here.
from authors.models import User

class Post(models.Model):
    type = models.CharField(max_length=255, default="post")

    # title of a post
    title = models.CharField(max_length=255, default="")

    # id of the post
    id = models.CharField(max_length=255, primary_key=True, default="")

    # where did you get this post from?
    source = models.URLField(default="")

    # where is it actually from
    origin = models.URLField(default="")

    #a brief description of the post
    description = models.TextField(default="")

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

    # the author has an ID where by authors can be disambiguated
    author_id = models.CharField(max_length=255, default="") # Author should be embedded (change later)
    
    # total number of comments for this post
    count = models.IntegerField(default=0)

    # the first page of comments
    comments = models.CharField(max_length=255, default="")

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

    # ISO 8601 TIMESTAMP
    published = models.DateTimeField(auto_now_add=True)

    # visibility ["PUBLIC","FRIENDS","UNLISTED"]
    visibility = models.CharField(max_length=20, default="UNLISTED")
    # for visibility PUBLIC means it is open to the wild web
    # FRIENDS means if we're friends I can see the post
    # FRIENDS should've already been sent the post so they don't need this

