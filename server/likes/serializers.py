from rest_framework import serializers
from .models import CommentLikes, PostLikes, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["type", "id", "host", "displayName", "url", "github", "profileImage"]


class LikesSerializerComment(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = CommentLikes
        fields = "__all__"

    def to_representation(self, instance):
        """Represents the object field as an url"""
        data = super().to_representation(instance)
        context = self.context
        base_url = context.get("base_url")
        if base_url is not None:
            author_id = instance.author.id
            post_id = instance.post.id
            comment_id = instance.id
            data["object"] = (
                f"{base_url}authors/{author_id}/posts/{post_id}/comments/{comment_id}"
            )
            data["summary"] = f"{instance.author.displayName} likes your comment"
        return data


class LikesSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = "__all__"

    def to_representation(self, instance):
        """Represents the object field as an url"""
        data = super().to_representation(instance)
        context = self.context
        base_url = context.get("base_url")
        if base_url is not None:
            author_id = instance.author.id
            post_id = instance.post.id
            data["object"] = f"{base_url}authors/{author_id}/posts/{post_id}"
            data["summary"] = f"{instance.author.displayName} likes your post"
        return data
