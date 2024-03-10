from django.db import models
from authors.models import Author

class Approval(models.Model):
    new_user = models.ForeignKey(
            Author, related_name="new_user", on_delete=models.CASCADE, default="None"
        )
    
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Approval for {self.new_user.email}"
  
