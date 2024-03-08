from rest_framework import serializers
from .models import SharedPost


class SharedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedPost
        fields = "__all__"

    def create(self, validated_data):
        return SharedPost.objects.create(**validated_data)
