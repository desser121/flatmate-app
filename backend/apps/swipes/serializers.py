from rest_framework import serializers
from .models import Swipe
from django.contrib.auth import get_user_model

User = get_user_model()


class SwipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Swipe
        fields = ['id', 'target_type', 'target_id', 'action', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class SwipeTargetSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    age = serializers.IntegerField(allow_null=True)
    city = serializers.CharField()
    photo = serializers.URLField(allow_blank=True, allow_null=True)
    compatibility = serializers.FloatField()
    type = serializers.ChoiceField(choices=['user', 'listing'])
    listing_type = serializers.CharField(allow_blank=True, allow_null=True)
    property_type = serializers.CharField(allow_blank=True, allow_null=True)
    budget_min = serializers.IntegerField(allow_null=True)
    budget_max = serializers.IntegerField(allow_null=True)
    description = serializers.CharField(allow_blank=True, allow_null=True)
