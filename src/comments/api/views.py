from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.contenttypes.models import ContentType


from posts.api.permissions import IsOwner

from .serializers import CommentListSerializers, CommentDetailSerializers, create_comment_serializer
from comments.models import Comments
from posts.models import Post


class CommentListAPIView(ListAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentListSerializers
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['user__username', 'content',
                       'timestamp', 'content_object__title']
    filterset_fields = ['user__username', 'content']
    search_fields = ['user__username', 'content']


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    """detail az Model e Comment besoorate API"""
    queryset = Comments.objects.all()
    serializer_class = CommentDetailSerializers
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]


class CommentCreateAPIView(CreateAPIView):
    queryset = Comments.objects.all()
    # serializer_class = CommentListSerializers
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     """User e har posti ke create mishe request.user"""
    # serializer.save(user=self.request.user)

    def get_serializer_class(self):
        # post = Post.objects.filter(published=True)
        model_type = self.request.GET.get("type")
        object_id = self.request.GET.get("id")
        # content = self.request.POST["content"]
        parent_id = self.request.GET.get("parent_id", None)
        # model_type = model_type.model_class()
        # if model_type == 'post':
        #     post = Post.objects.get(id=object_id)
        # model = ContentType.objects.get_for_model(post.__class__)
        return create_comment_serializer(instance=model_type, object_id=object_id, parent_id=parent_id, user=self.request.user)
