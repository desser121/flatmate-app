from rest_framework import generics, permissions
from django.utils import timezone
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            match__user1=user
        ) | Conversation.objects.filter(
            match__user2=user
        )


class ConversationDetailView(generics.RetrieveAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            match__user1=user
        ) | Conversation.objects.filter(
            match__user2=user
        )


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            conversation_id=self.kwargs['conversation_id']
        )

    def perform_create(self, serializer):
        message = serializer.save(
            author=self.request.user,
            conversation_id=self.kwargs['conversation_id'],
        )
        conversation = message.conversation
        conversation.last_message_at = timezone.now()
        conversation.save()


class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        message = serializer.save(
            author=self.request.user,
            conversation_id=self.kwargs['conversation_id'],
        )
        conversation = message.conversation
        conversation.last_message_at = timezone.now()
        conversation.save()
