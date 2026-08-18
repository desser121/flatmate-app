from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConversationListView.as_view(), name='conversation-list'),
    path('<uuid:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
    path('<uuid:conversation_id>/messages/', views.MessageListView.as_view(), name='message-list'),
    path('<uuid:conversation_id>/messages/create/', views.MessageCreateView.as_view(), name='message-create'),
]
