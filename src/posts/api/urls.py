from django.urls import path
from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostDeleteAPIView,
    PostUpdateAPIView,
    PostCreateAPIView
)

urlpatterns = [
    path("", PostListAPIView.as_view(), name='post-list-api'),
    path("create/", PostCreateAPIView.as_view(), name='post-create-api'),
    path("detail/<int:pk>/", PostDetailAPIView.as_view(), name='post-detail-api'),
    path("update/<int:pk>/", PostUpdateAPIView.as_view(), name='post-update-api'),
    path("delete/<int:pk>/", PostDeleteAPIView.as_view(), name='post-delete-api'),
]
