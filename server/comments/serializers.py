from rest_framework import serializers
from .models import Comment, Author

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class AuthorRefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
