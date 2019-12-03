from django.urls import path
from .views import LikeListAPIView, LikeDetailAPIView, LikeCreateAPIView

urlpatterns = [
    path("", LikeListAPIView.as_view(), name='like-list-api'),
    path("<int:pk>/", LikeDetailAPIView.as_view(), name='like-detail-api'),
    path("like/add/", LikeCreateAPIView.as_view(), name='like-create-api'),
]
