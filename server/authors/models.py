from django.db import models


# Create your models here.

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