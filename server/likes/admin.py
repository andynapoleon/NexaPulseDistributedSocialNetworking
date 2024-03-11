from django.contrib import admin
from .models import CommentLikes, PostLikes

# Register your models here.
admin.site.register(CommentLikes)
admin.site.register(PostLikes)