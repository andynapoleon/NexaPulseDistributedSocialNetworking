from rest_framework import serializers
from .models import Authors

class AuthorsSerializer(serializers.Serializer):
    id = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()  # This will be encripted
    github = serializers.CharField()
    profileImage = serializers.ImageField()

    def create(self, validated_data):
        """
        Create and return a new `Authors` instance, given the validated data
        """
        return Authors.object.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Authors` instance, given the validated data
        """
        instance.firstName = validated_data.get('firstName', instance.firstName)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.github = validated_data.get('github', instance.github)
        instance.profileImage = validated_data.get('profileImage', instance.profileImage)
        instance.save()
        return instance