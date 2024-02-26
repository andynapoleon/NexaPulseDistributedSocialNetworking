from rest_framework import serializers
from .models import Follows  # Import your Follows model

class FollowsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follows
        fields = '__all__'  # You can specify the fields you want to include here
