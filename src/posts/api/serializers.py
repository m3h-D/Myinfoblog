from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from urllib.parse import urlsplit
from posts.models import Post
from comments.api.serializers import CommentListSerializers
from comments.models import Comments


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    detail = serializers.HyperlinkedIdentityField(
        view_name='posts-api:post-detail-api'
    )
    delete = serializers.HyperlinkedIdentityField(
        view_name='posts-api:post-delete-api'
    )

    class Meta:
        model = Post
        fields = ('id', 'avatar', 'delete', 'detail', 'title',
                  'author', 'image', 'content',)

    def get_author(self, obj):
        return str(obj.author.username)

    def get_avatar(self, obj):
        request = self.context['request']
        current_site = get_current_site(request)
        protocol = urlsplit(request.build_absolute_uri(None)).scheme
        a = (protocol + "://", current_site.domain, obj.author.profile.image.url)
        return ''.join(a)


class PostDetailSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    delete = serializers.HyperlinkedIdentityField(
        view_name='posts-api:post-delete-api'
    )

    class Meta:
        model = Post
        fields = '__all__'
        # exclude = ('id', )

    def get_author(self, obj):
        return obj.author.username

    def get_avatar(self, obj):
        request = self.context['request']
        current_site = get_current_site(request)
        protocol = urlsplit(request.build_absolute_uri(None)).scheme
        a = (protocol + "://", current_site.domain, obj.author.profile.image.url)
        return ''.join(a)

    def get_comments(self, obj):
        post_comments = obj.comments
        comments = CommentListSerializers(
            post_comments, many=True, context=self.context).data
        return comments


class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        exclude = ('id', 'read_time', 'slug', 'author')
