from django.db import models

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50, default="")
    lastName = models.CharField(max_length=50, default="")
    email = models.EmailField(default="unknown@example.com", unique=True)
    password = models.CharField(max_length=255, default="")  # This will be encripted
    github = models.CharField(max_length=100, default="")
    profileImage = models.ImageField(
        upload_to="assets/profile_images/", null=True, blank=True
    )

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

    def check_password(self, client_password):
        return self.password == client_password


class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    public = models.BooleanField()
    content = models.TextField()
    # Add more fields as needed


class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()


class Like(models.Model):
    lid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


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

    class Meta:
        unique_together = (("follower", "followed"),)


class MakesPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class HasComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(MakesPost, on_delete=models.CASCADE)


class OwnComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class OwnLike(models.Model):
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
