from django.contrib import admin
from .models import Author, Comment, Like, FollowedBy, Follows, Post

# Register your models here.
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(FollowedBy)
admin.site.register(Follows)
admin.site.register(Post)