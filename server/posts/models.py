from django.db import models

# Create your models here.
from authors.models import Authors

class Post(models.Model):
    id = models.CharField(max_length=255, primary_key=True, default="")
    # title = models.CharField(max_length=255)
    # source = models.URLField()
    # origin = models.URLField()
    # description = models.TextField()
    # content_type = models.CharField(max_length=50)
    # content = models.TextField()
    # author_id = models.CharField(max_length=255)
    published = models.DateTimeField(auto_now_add=True)
    # visibility = models.CharField(max_length=20)
