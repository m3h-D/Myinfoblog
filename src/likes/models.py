from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.template.defaultfilters import truncatewords_html, truncatewords, truncatechars_html
from django.utils.html import strip_tags

from .utils import get_client_ip, likedislike_manager
# Create your models here.


User = get_user_model()


class LikeDislikeManager(models.Manager):
    """mesle manager e Comments"""

    def filter_by_model(self, instance):
        """bar assasse model filter mikonim"""
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        queryset = super(LikeDislikeManager, self).filter(
            content_type=content_type, object_id=obj_id)
        return queryset

    # liked, disliked
    def create_for_instance_model(self, instance, request, likedislike):
        """
        bar assasse model create mkonim
        age user anonymous bud bar assasse IP_address taghirat emal mishe
        age authenticate bud ke nega mikone bebine ip sh hast ya na age bud
        faqat user behesh mide...
        """

        user = request.user
        ip_address = get_client_ip(request)
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        content = instance.content

        # liked_or_not = self.filter_by_model(instance=instance).filter(
        #     ip_address=ip_address, likedislike='like').first()
        # disliked_or_not = self.filter_by_model(instance=instance).filter(
        #     ip_address=ip_address, likedislike='dislike').first()
        if request.user.is_authenticated:
            # queryset = super(LikeDislikeManager, self).get_or_create()
            try:
                queryset = self.get(
                    user=user,
                    ip_address=ip_address,
                    content_type=content_type,
                    object_id=obj_id,
                    content=content,
                )
                likedislike_manager(queryset, likedislike)

            except:
                queryset = self.create(
                    user=user,
                    ip_address=ip_address,
                    content_type=content_type,
                    object_id=obj_id,
                    content=content,
                    # liked=liked,
                    # disliked=disliked,
                    likedislike=likedislike,
                )
        elif request.user.is_anonymous:

            try:
                queryset = self.get(
                    ip_address=ip_address,
                    content_type=content_type,
                    object_id=obj_id,
                    content=content,
                )
                likedislike_manager(queryset, likedislike)
                # if queryset.likedislike == 'like' and likedislike == 'like':
                #     queryset.delete()
                # elif queryset.likedislike == 'dislike' and likedislike == 'dislike':
                #     queryset.delete()
                # elif queryset.likedislike == 'like' and likedislike == 'dislike':
                #     queryset.likedislike = 'dislike'
                #     queryset.save()
                # elif queryset.likedislike == 'dislike' and likedislike == 'like':
                #     queryset.likedislike = 'like'
                #     queryset.save()
            except:
                queryset = self.create(
                    ip_address=ip_address,
                    content_type=content_type,
                    object_id=obj_id,
                    content=content,
                    # liked=liked,
                    # disliked=disliked,
                    likedislike=likedislike,
                )

        # if liked_or_not:
        #     liked_or_not.delete()
        # if disliked_or_not:
        #     disliked_or_not.delete()
        return queryset


class LikeDislike(models.Model):
    """modeli baraye like o dislike eyek post ya comment"""
    user = models.ForeignKey(User, related_name='likedislike', blank=True, null=True,
                             on_delete=models.CASCADE, verbose_name='کاربر')
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='ایدی قسمت')
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField(blank=True, default='text', verbose_name='متن')
    # liked = models.BooleanField(default=False, verbose_name='دوست داشته')
    # disliked = models.BooleanField(default=False, verbose_name='دوست نداشته')
    LIKED_OR_DISLIKE = (
        ('like', 'دوست دارد'),
        ('dislike', 'دوست ندارد'),
    )
    likedislike = models.CharField(
        max_length=10, blank=True, choices=LIKED_OR_DISLIKE, verbose_name='دوست/نه دوست')
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = LikeDislikeManager()

    class Meta:
        """order kardan bar assasse timestamp"""
        ordering = ('-timestamp',)
        verbose_name = "لایک/دیس لایک"
        verbose_name_plural = " لایک ها /دیس لایک ها"

    @property
    def short_content(self):
        return strip_tags(truncatewords(self.content, 5))

    def __str__(self):
        try:
            return self.user.username
        except:
            return self.ip_address
