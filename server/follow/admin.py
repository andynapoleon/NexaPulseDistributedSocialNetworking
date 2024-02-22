from django.contrib import admin
from .models import FollowedBy, Follows
# Register your models here.
admin.site.register(FollowedBy)
admin.site.register(Follows)
