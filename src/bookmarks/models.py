from django.db import models
from django.shortcuts import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class BookMarkManager(models.Manager):
    """filter kardane object bar assasse model"""

    def filter_by_model(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        queryset = super(BookMarkManager, self).filter(
            content_type=content_type, object_id=object_id)

        return queryset

    def create_by_instance_model(self, user, instance):
        """agar hamchin posti(model) baraye user bud hazfesh kon age nabud create kon"""
        content_type = ContentType.objects.get_for_model(instance.__class__)
        try:
            queryset = BookMark.objects.filter_by_model(
                instance=instance).get(user=user)
            queryset.delete()
        except BookMark.DoesNotExist:
            queryset = super(BookMarkManager, self).create(
                user=user,
                content_type=content_type,
                object_id=instance.id,
            )
        return queryset


class BookMark(models.Model):
    """baraye zakhire kardane ye Post(model, favorite)"""
    user = models.ForeignKey(
        User, related_name='bookmark', on_delete=models.CASCADE, verbose_name='کاربر')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BookMarkManager()

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'مارک شده'
        verbose_name_plural = 'مارک شده ها'

    def __str__(self):
        try:
            return ("{} پست {} را مارک کرده.").format(self.user.username, self.content_object.title)
        except:
            return self.user.username

    # def get_delete_url(self):
    #     return reverse("bookmarks:add-to-bookmarke", args=[self.object_id])
