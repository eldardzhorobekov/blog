from rest_framework import serializers
from main.models import Profile

class FollowUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    is_following = serializers.BooleanField(required=True)