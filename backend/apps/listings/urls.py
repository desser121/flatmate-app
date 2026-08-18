from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListingListCreateView.as_view(), name='listing-list'),
    path('<uuid:pk>/', views.ListingDetailView.as_view(), name='listing-detail'),
    path('<uuid:listing_id>/photos/', views.ListingPhotoUploadView.as_view(), name='listing-photo-upload'),
]
