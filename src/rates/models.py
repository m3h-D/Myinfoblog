from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class RateManager(models.Manager):
    def filter_by_model(self, instance):
        """filter kardane content bar assasse model"""
        content_type = ContentType.objects.get_for_model(instance.__class__)
        queryset = super(RateManager, self).filter(
            content_type=content_type, object_id=instance.id)
        return queryset


class Rate(models.Model):
    """modele emtiaz (rating star)"""
    user = models.ForeignKey(User, related_name="rate",
                             on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    RATING_LEVEL = (
        (1, 'خیلی بد'),
        (2, 'بد'),
        (3, 'متوسط'),
        (4, 'خوب'),
        (5, 'خیلی خوب'),
    )
    rating = models.IntegerField(choices=RATING_LEVEL, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = RateManager()

    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیاز ها"

    def __str__(self):
        return ("{} به ( {} ) امتیاز ( {} ) داده").format(self.user.username, self.content_object.title, self.get_rating_display())
