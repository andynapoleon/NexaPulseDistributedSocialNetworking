from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        '''Represents the id field as an url'''
        data = super().to_representation(instance)
        context = self.context
        base_url = context.get('base_url')
        if base_url is not None:
            author_id = instance.author.id
            post_id = instance.post.id
            if data['contentType'] == "image/png;base64" or data['contentType'] == "image/jpeg;base64":
                data['id'] = f"{base_url}authors/{author_id}/posts/{post_id}/image"
            else:
                data['id'] = f"{base_url}authors/{author_id}/posts/{post_id}/"
        return data