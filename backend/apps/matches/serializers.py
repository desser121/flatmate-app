from rest_framework import serializers
from .models import Match
from apps.users.serializers import UserPublicSerializer


class MatchSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['id', 'other_user', 'listing', 'created_at']

    def get_other_user(self, obj):
        request_user = self.context['request'].user
        other = obj.user2 if obj.user1 == request_user else obj.user1
        from apps.users.serializers import UserPublicSerializer
        return UserPublicSerializer(other).data
