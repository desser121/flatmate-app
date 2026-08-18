from django.urls import path
from . import views

urlpatterns = [
    path('', views.MatchListView.as_view(), name='match-list'),
    path('<uuid:pk>/', views.MatchDetailView.as_view(), name='match-detail'),
]
