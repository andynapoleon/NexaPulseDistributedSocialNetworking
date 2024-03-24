from rest_framework import serializers
from .models import Post
from authors.serializers import AuthorSerializer
from comments.serializers import CommentSerializer
from markdownx.utils import markdownify


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(source="authorId")
    comments = CommentSerializer()

    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        """Represents the id field as an url"""
        data = super().to_representation(instance)
        context = self.context
        base_url = context.get("base_url")
        if base_url is not None:
            author_id = instance.authorId. 
            post_id = instance.id
            data["comments"] = f"{base_url}authors/{author_id}/posts/{post_id}/comments"
            if (
                data["contentType"] == "image/png;base64"
                or data["contentType"] == "image/jpeg;base64"
            ):
                data["id"] = f"{base_url}authors/{author_id}/posts/{post_id}/image"
            else:
                data["id"] = f"{base_url}authors/{author_id}/posts/{post_id}"

            if data["contentType"] == "text/markdown":
                data["content"] = markdownify(data["content"])

        return data


class ServerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
