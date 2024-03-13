from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['type', 'id', 'host', 'displayName', 'url', 'github', 'profileImage']

        def to_representation(self, instance):
            '''Represents the id field as an url'''
            data = super().to_representation(instance)
            context = self.context
            base_url = context.get('base_url')
            print("here:", base_url)
            if base_url is not None:
                author_id = instance.author.id
                data['id'] = f"{base_url}authors/{author_id}"
                data['url'] = f"{base_url}authors/{author_id}"
                data['host'] = f"{base_url}"
            return data

   