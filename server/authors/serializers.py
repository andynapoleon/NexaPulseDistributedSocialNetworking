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
