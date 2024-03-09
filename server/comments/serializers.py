from rest_framework import serializers
from .models import Comment, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'email', 'firstName', 'lastName', 'github', 'profileImage']

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Comment
        fields = ['type', 'author', 'comment', 'content_type', 'published', 'id']

    def to_representation(self, instance):
        '''Represents the id field as an url'''
        data = super().to_representation(instance)
        context = self.context
        base_url = context.get('base_url')
        if base_url is not None:
            author_id = instance.author.id
            post_id = instance.post.id
            comment_id = instance.id
            data['id'] = f"{base_url}authors/{author_id}/posts/{post_id}/comments/{comment_id}"
        return data
    
class CommentSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new `Post` instance, given the validated data
        """
        return Comment.objects.create(**validated_data)
