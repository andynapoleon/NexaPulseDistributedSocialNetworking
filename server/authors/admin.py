from django.contrib import admin
from .models import Author, User, FollowedBy, Follows

# Register your models here.
admin.site.register(Author)
admin.site.register(User)
# admin.site.register(Comment)
# admin.site.register(Like)
admin.site.register(FollowedBy)
admin.site.register(Follows)
# admin.site.register(Post)