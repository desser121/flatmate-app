from django.urls import path
from . import views

urlpatterns = [
    path('', views.SwipeCreateView.as_view(), name='swipe-create'),
    path('undo/', views.SwipeUndoView.as_view(), name='swipe-undo'),
    path('feed/', views.FeedView.as_view(), name='feed'),
]
