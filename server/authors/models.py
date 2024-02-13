from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100, default='')

class User(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    email = models.EmailField(default="unknown@example.com", unique=True)
    password = models.CharField(max_length=255, default='') # This will be encripted
    github = models.CharField(max_length=100, default='')
    profileImage = models.ImageField(upload_to='assets/profile_images/', null=True, blank=True) 
    # for debugging:
    # def __str__(self):
    #     return f"{self.firstname} {self.lastname}"

class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Like(models.Model):
    lid = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class FollowedBy(models.Model):
    id1 = models.ForeignKey(User, related_name='follows', on_delete=models.CASCADE)
    id2 = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('id1', 'id2')

class Follows(models.Model):
    follower = models.ForeignKey(User, related_name='follower_set', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed_set', on_delete=models.CASCADE)

    # class Meta:
    #     unique_together = (('follower', 'followed'),)

class Post(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.CharField(primary_key=True, max_length=50)
    public = models.BooleanField()
    # Add more fields as needed

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
