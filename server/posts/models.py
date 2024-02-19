from django.db import models

# Create your models here.
from authors.models import User

class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)  # Default to False, since posts should be private by default
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.pid} by {self.author}"
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post} - {self.created_at}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.author} on {self.post} - {self.created_at}"
    
class MakesPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class HasComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    post = models.ForeignKey(MakesPost, on_delete=models.CASCADE)


class OwnComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OwnLike(models.Model):
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
