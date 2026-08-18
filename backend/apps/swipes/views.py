from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .models import Swipe
from .serializers import SwipeSerializer

User = get_user_model()


class SwipeCreateView(generics.CreateAPIView):
    serializer_class = SwipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        swipe = serializer.save()

        from apps.matches.services import check_and_create_match
        match = check_and_create_match(swipe)

        result = SwipeSerializer(swipe).data
        if match:
            result['match_created'] = True
            result['match_id'] = str(match.id)

        return Response(result, status=status.HTTP_201_CREATED)


class SwipeUndoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        swipe = Swipe.objects.filter(
            author=request.user, is_active=True
        ).order_by('-created_at').first()

        if swipe:
            swipe.is_active = False
            swipe.save()
            return Response({'status': 'undone'})

        return Response({'status': 'nothing_to_undo'}, status=status.HTTP_404_NOT_FOUND)


class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        target_type = request.query_params.get('type', 'user')
        page = int(request.query_params.get('page', 1))
        page_size = 20

        from apps.recommendations.services import get_feed
        feed = get_feed(user, target_type)

        start = (page - 1) * page_size
        end = start + page_size

        return Response({
            'items': feed[start:end],
            'page': page,
            'has_more': end < len(feed),
            'total': len(feed),
        })
