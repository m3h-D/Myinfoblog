from rest_framework import serializers

from likes.models import LikeDislike


class LikeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = LikeDislike
        fields = ('id', 'user', 'content', 'liked', 'disliked',)
