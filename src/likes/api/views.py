from rest_framework.generics import ListAPIView, RetrieveAPIView

from likes.models import LikeDislike
from .serializers import LikeListSerializer


class LikeListAPIView(ListAPIView):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeListSerializer


class LikeDetailAPIView(RetrieveAPIView):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeListSerializer
