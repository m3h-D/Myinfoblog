from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.template.defaultfilters import truncatewords_html, truncatewords, truncatechars_html
from django.utils.html import strip_tags

from .utils import get_client_ip
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

    def create_for_instance_model(self, instance, request, liked, disliked):
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
        disliked_or_not = self.filter_by_model(
            instance=instance).filter(ip_address=ip_address, disliked=True).first()

        liked_or_not = self.filter_by_model(
            instance=instance).filter(ip_address=ip_address, liked=True).first()
        if request.user.is_authenticated:
            queryset = super(LikeDislikeManager, self).get_or_create(
                user=user,
                ip_address=ip_address,
                content_type=content_type,
                object_id=obj_id,
                content=content,
                liked=liked,
                disliked=disliked,
            )
        elif request.user.is_anonymous:
            # disliked_or_not = self.filter_by_model(
            #     instance=instance).filter(ip_address=ip_address, disliked=True).first()

            # liked_or_not = self.filter_by_model(
            #     instance=instance).filter(ip_address=ip_address, liked=True).first()
            try:
                queryset = super(LikeDislikeManager, self).get(
                    ip_address=ip_address,
                    content_type=content_type,
                    object_id=obj_id,
                    content=content,
                    liked=liked,
                    disliked=disliked,
                )
            except:
                queryset = super(LikeDislikeManager, self).create(
                    ip_address=ip_address,
                    content_type=content_type,
                    object_id=obj_id,
                    content=content,
                    liked=liked,
                    disliked=disliked,
                )

        if liked_or_not:
            liked_or_not.delete()
        if disliked_or_not:
            disliked_or_not.delete()

        return queryset

    # def get_for_instance_model(self, instance, user, liked, disliked):
    #     """bar assasse model create mkonim"""
    #     content_type = ContentType.objects.get_for_model(instance.__class__)
    #     obj_id = instance.id
    #     queryset = super(LikeDislikeManager, self).filter(
    #         user=user,
    #         content_type=content_type,
    #         object_id=obj_id,
    #         liked=liked,
    #         disliked=disliked,
    #     ).first()

    #     if queryset.liked == True:
    #         queryset.delete()

    #     else:
    #         queryset.liked = True
    #         queryset.save()

    #     if queryset.disliked == True:
    #         queryset.delete()

    #     else:
    #         queryset.disliked = True
    #         queryset.save()
    #         if queryset.liked == True:
    #             queryset.delete()

    #     return queryset


class LikeDislike(models.Model):
    """modeli baraye like o dislike eyek post ya comment"""
    user = models.ForeignKey(User, related_name='likedislike', blank=True, null=True,
                             on_delete=models.CASCADE, verbose_name='کاربر')
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='ایدی قسمت')
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField(blank=True, default='text', verbose_name='متن')
    liked = models.BooleanField(default=False, verbose_name='دوست داشته')
    disliked = models.BooleanField(default=False, verbose_name='دوست نداشته')
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
        """ bargardandane name karbar noe object va like ya dislike"""
        try:
            if self.liked:
                return "{} پست ({}) را دوست دارد".format(self.user.username, self.content_object.title)
            elif self.disliked:
                return "{} پست ({}) را دوست ندارد".format(self.user.username, self.content_object.title)
        except:
            if self.liked:
                return "{} کامنت ({}) را دوست دارد".format(self.user.username, self.content_object.content)
            elif self.disliked:
                return "{} کامنت ({}) را دوست ندارد".format(self.user.username, self.content_object.content)
        finally:
            if self.liked:
                return "{}   را دوست دارد".format(self.ip_address)
            elif self.disliked:
                return "{}   را دوست ندارد".format(self.ip_address)
