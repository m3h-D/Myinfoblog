from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from likes.models import LikeDislike
from .serializers import LikeListSerializer, create_likedislike_serializer


class LikeListAPIView(ListAPIView):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeListSerializer


class LikeDetailAPIView(RetrieveAPIView):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeListSerializer


class LikeCreateAPIView(CreateAPIView):
    queryset = LikeDislike.objects.all()

    def get_serializer_class(self):
        model_type = self.request.GET.get("content_type")
        object_id = self.request.GET.get("object_id")

        return create_likedislike_serializer(instance=model_type, object_id=object_id, request=self.request)
