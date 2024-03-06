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
        # Either we pass in the base url i.e, http://127.0.0.1:8000/ or find a way to get it
        data = super().to_representation(instance)
        author_id = instance.author.id
        post_id = instance.post.id
        comment_id = instance.id
        data['id'] = f"/authors/{author_id}/posts/{post_id}/comments/{comment_id}"
        return data
