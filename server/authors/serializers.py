from rest_framework import serializers
from .models import Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Authors` instance, given the validated data
        """
        return Author.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and return an existing `Author` instance, given the validated data
        """
        instance.email = validated_data.get('email', instance.email)
        instance.firstName = validated_data.get('firstName', instance.firstName)
        instance.lastName = validated_data.get('lastName', instance.lastName)
        instance.github = validated_data.get('github', instance.github)
        instance.profileImage = validated_data.get('profileImage', instance.profileImage)
        instance.lastUpdated = validated_data.get('lastUpdated', instance.lastUpdated)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_staff = validated_data.get('is_staff', instance.is_staff)
        instance.save()
        return instance
