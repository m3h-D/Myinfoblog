from rest_framework import serializers

from django.contrib.contenttypes.models import ContentType

from likes.models import LikeDislike


class LikeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeDislike
        fields = ('id', 'user', 'content', 'likedislike',)


def create_likedislike_serializer(instance, object_id, request):
    class LikeDislikeSerializer(serializers.ModelSerializer):
        class Meta:
            model = LikeDislike
            fields = ('likedislike',)

        def __init__(self, *args, **kwargs):
            self.model_type = instance
            self.object_id = object_id
            super().__init__(*args, **kwargs)

        def validate(self, data):
            content_type = ContentType.objects.get(model=self.model_type)
            if not content_type:
                raise serializers.ValidationError(
                    "چنین مدلی موجود نیست")
            Model = content_type.model_class()
            model_qs = Model.objects.get(id=self.object_id)
            if not model_qs:
                raise serializers.ValidationError(
                    "چنین ای دی برای این مدل موجود نیست")
            return data

        def create(self, validated_data):
            content_type = ContentType.objects.get(model=self.model_type)
            Model = content_type.model_class()
            model_qs = Model.objects.get(id=self.object_id)
            likedislike = validated_data.get("likedislike")
            like_create = LikeDislike.objects.create_for_instance_model(
                # like_create = LikeDislike.objects.create_for_instance_model_api(
                # instance=self.model_type, id=self.object_id, content=model_qs.content, request=request, likedislike=likedislike)
                instance=model_qs, request=request, likedislike=likedislike)
            return like_create
    return LikeDislikeSerializer
