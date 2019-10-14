from django.urls import path

from .views import CommentListAPIView, CommentDetailAPIView, CommentCreateAPIView


urlpatterns = [
    path('', CommentListAPIView.as_view(), name='comment-list-api'),
    path('create/', CommentCreateAPIView.as_view(), name='comment-create-api'),
    path('detail/<int:pk>/', CommentDetailAPIView.as_view(),
         name='comment-detail-api'),
]
