from rest_framework import serializers
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'author', 'author_name', 'content', 'message_type',
                  'attachment_url', 'is_read', 'created_at']
        read_only_fields = ['id', 'author', 'is_read', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'match', 'other_user', 'last_message', 'unread_count',
                  'last_message_at', 'created_at']

    def get_other_user(self, obj):
        request_user = self.context['request'].user
        other = obj.match.user2 if obj.match.user1 == request_user else obj.match.user1
        from apps.users.serializers import UserPublicSerializer
        return UserPublicSerializer(other).data

    def get_last_message(self, obj):
        msg = obj.messages.order_by('-created_at').first()
        if msg:
            return {
                'content': msg.content[:100],
                'message_type': msg.message_type,
                'created_at': msg.created_at,
            }
        return None

    def get_unread_count(self, obj):
        return obj.messages.filter(is_read=False).exclude(
            author=self.context['request'].user
        ).count()
