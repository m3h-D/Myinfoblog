from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    # UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)


from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Post
from .serializers import PostListSerializer, PostDetailSerializer, PostCreateSerializer
from .permissions import IsOwner
from .pagination import PostNumberPagination


class PostCreateAPIView(CreateAPIView):
    """sakhte yek Post besoorate API"""
    queryset = Post.objects.filter(published=True)
    serializer_class = PostCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        """User e har posti ke create mishe request.user"""
        serializer.save(author=self.request.user)


class PostListAPIView(ListAPIView):
    """Listi az Model e Post besoorate API"""
    queryset = Post.objects.filter(published=True)
    serializer_class = PostListSerializer
    # pagination_class = PostNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['title', 'author__username', 'special', 'created']
    filterset_fields = ['category__title', 'special', 'author__username']
    search_fields = ['title', 'content', 'category__title']


class PostDetailAPIView(RetrieveAPIView):
    """detail az Model e Post besoorate API"""
    queryset = Post.objects.filter(published=True)
    serializer_class = PostDetailSerializer


class PostUpdateAPIView(RetrieveUpdateDestroyAPIView):
    """update kardane yek post"""
    queryset = Post.objects.filter(published=True)
    serializer_class = PostDetailSerializer
    permission_classes = [IsOwner]

    # def perform_update(self, serializer):
    #     """User e har posti ke create mishe request.user"""
    #     serializer.save(author=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    """update kardane yek post"""
    queryset = Post.objects.filter(published=True)
    serializer_class = PostDetailSerializer
    permission_classes = [IsAdminUser]
