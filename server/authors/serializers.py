from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.Serializer):
    name = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new `Author` instance, given the validated data
        """
        return Author.object.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Author` instance, given the validated data
        """
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance