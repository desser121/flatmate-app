from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('me/photos/', views.UserPhotoUploadView.as_view(), name='user-photo-upload'),
    path('me/photos/<uuid:id>/', views.UserPhotoDeleteView.as_view(), name='user-photo-delete'),
    path('me/preferences/', views.PreferenceView.as_view(), name='user-preferences'),
    path('<uuid:id>/', views.UserDetailView.as_view(), name='user-detail'),
]
