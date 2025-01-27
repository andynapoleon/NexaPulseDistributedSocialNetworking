from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["type", "id", "host", "displayName", "url", "github", "profileImage"]

    def to_representation(self, instance):
        """Represents the id field as an url"""
        data = super().to_representation(instance)
        print(data)
        context = self.context
        base_url = context.get("base_url")
        if base_url is not None:
            author_id = instance.id
            data["id"] = f"{base_url}authors/{author_id}"
            data["url"] = f"{base_url}authors/{author_id}"
        return data
