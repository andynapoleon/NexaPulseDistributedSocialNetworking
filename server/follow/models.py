from django.db import models
from authors.models import Author
# Create your models here.

class FollowedBy(models.Model):
    id1 = models.ForeignKey(Author, related_name="follows", on_delete=models.CASCADE)
    id2 = models.ForeignKey(Author, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("id1", "id2")

class Follows(models.Model):
    follower = models.ForeignKey(
        Author, related_name="follower_set", on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        Author, related_name="followed_set", on_delete=models.CASCADE
    )

    acceptedRequest = models.BooleanField(default=False)  # Added boolean field

    class Meta:
        unique_together = (("follower", "followed"),)