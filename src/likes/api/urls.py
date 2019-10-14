from django.urls import path
from .views import LikeListAPIView, LikeDetailAPIView

urlpatterns = [
    path("", LikeListAPIView.as_view(), name='like-list-api'),
    path("<int:pk>/", LikeDetailAPIView.as_view(), name='like-detail-api'),
]
