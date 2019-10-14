from rest_framework import serializers
from comments.models import Comments, CommentManager
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
# from generic_relations.relations import GenericRelatedField
from posts.models import Post


User = get_user_model()


def create_comment_serializer(user, object_id, instance, parent_id=None):
    # def create_comment_serializer(instance, parent_id=None, user=None):
    class CommentCreateSrializer(serializers.ModelSerializer):
        class Meta:
            model = Comments
            fields = ("content",)

        def __init__(self, *args, **kwargs):
            self.content_type = instance
            self.object_id = object_id
            self.parent_obj = None
            if parent_id:
                parent_qs = Comments.objects.filter(id=parent_id)
                if parent_qs.exists():
                    self.parent_obj = parent_qs.first()
            super(CommentCreateSrializer, self).__init__(*args, **kwargs)
            # return qs

        def validate(self, data):
            content_type = self.content_type
            object_id = self.object_id
            # model_qs = Post.objects.all()
            model_qs = ContentType.objects.get(model=content_type)
            if not model_qs:
                raise serializers.ValidationError(
                    "this is not a valid content type")
            SomeModel = model_qs.model_class()
            # obj_qs = Post.objects.filter(id=self.object_id)
            obj_qs = SomeModel.objects.filter(id=object_id)
            if not obj_qs.exists():
                raise serializers.ValidationError(
                    "This id for this model does not exists")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            # instance = self.instance
            content_type = self.content_type
            object_id = self.object_id
            parent_obj = self.parent_obj
            # obj_qs = Post.objects.get(id=object_id)
            if user:
                minuser = user
            else:
                minuser = User.objects.all().first()

            comment = Comments.objects.form_create_by_model(
                instance=content_type, object_id=object_id, user=minuser, content=content, parent_obj=parent_obj)
            return comment

    return CommentCreateSrializer


class CommentListSerializers(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    detaile = serializers.HyperlinkedIdentityField(
        view_name='comments-api:comment-detail-api'
    )

    class Meta:
        model = Comments
        exclude = ['content_type', 'object_id', 'parent']

    def get_user(self, obj):
        return obj.user.username

    def get_avatar(self, obj):
        a = ('http://127.0.0.1:8000', obj.user.profile.image.url)
        return ''.join(a)

    def get_reply_count(self, obj):
        try:
            return obj.children().count()
        except:
            return 0


class CommentDetailSerializers(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    content_object_url = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        exclude = ['content_type', 'object_id']
        read_only_fields = [
            # 'content_type',
            # 'object_id',
            'parent',
            'uuid',
            'reply_count',
            'user',
            'avatar'
        ]

    def get_content_object_url(self, obj):
        a = ('http://127.0.0.1:8000', obj.content_object.get_absolute_api_url())
        return ''.join(a)

    def get_user(self, obj):
        return obj.user.username

    def get_avatar(self, obj):
        a = ('http://127.0.0.1:8000', obj.user.profile.image.url)
        return ''.join(a)

    def get_replies(self, obj):
        if obj.parent:
            # try:
            return CommentListSerializers(obj.children(), many=True, context=self.context).data
        # except:
        return None

    def get_reply_count(self, obj):
        try:
            return obj.children().count()
        except:
            return 0
