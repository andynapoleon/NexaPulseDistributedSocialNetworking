from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
from SocialDistribution.settings import SERVER


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class Author(AbstractBaseUser):  # PermissionsMixin
    type = models.CharField(max_length=50, default="author", editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, default="")
    displayName = models.CharField(max_length=25, default="")
    url = models.URLField(editable=False, default="")
    # host = models.CharField(max_length=50, editable=False, default="")
    github = models.CharField(max_length=100, blank=True, default="")
    profileImage = models.URLField(default="https://i.imgur.com/V4RclNb.png")
    lastUpdated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    host = models.URLField(blank=True, default=SERVER, null=True)
    isForeign = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    # def check_password(self, client_password):
    #     return self.password == client_password
    def has_module_perms(self, app_label):
        # For simplicity, let's assume all authors have permission to all modules
        return True

    def has_perm(self, perm, obj=None):
        # For simplicity, let's assume all authors have all permissions
        return True

    @property
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


# Add related_name to avoid clashes
# Group.add_to_class(
#     "authors_group", models.ManyToManyField(Author, related_name="author_groups")
# )
# Permission.add_to_class(
#     "authors_permission",
#     models.ManyToManyField(Author, related_name="author_permissions"),
# )
