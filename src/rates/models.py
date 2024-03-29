from django.db import models
from django.db.models import Count, Avg
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

import logging
import sys

User = get_user_model()

# Create your models here.


def error_handling():
    return f"{sys.exc_info()[0]}. ({sys.exc_info()[1]}) in Line {sys.exc_info()[2].tb_lineno}"


class RateManager(models.Manager):
    def filter_by_model(self, instance):
        """filter kardane content bar assasse model"""
        content_type = ContentType.objects.get_for_model(instance.__class__)
        queryset = super(RateManager, self).filter(
            content_type=content_type, object_id=instance.id)
        return queryset

    def avg_rate(self, instance, avg=0):
        """emtiaz dehi be post bar assasse rate entekhab shude (az 1 ta 5) taghsim bar tedad e user haey ke be in post emtiaz dadan"""

        try:
            # user_count = self.filter_by_model(
            #     instance=instance).annotate(Count('user')).count()
            # avg = sum(x.rating for x in self.filter_by_model(
            #     instance=instance)) / int(user_count)
            my_avg = self.filter_by_model(
                instance).aggregate(Avg('rating'))
        except ZeroDivisionError:
            logging.error(error_handling())

        # f = ''
        # if avg <= 1.0:
        #     f = "خیلی بد"
        # if 1.0 <= avg < 3.0:
        #     f = "بد"
        # if 3.0 <= avg < 4.0:
        #     f = "متوسط"
        # if 4.0 <= avg < 5.0:
        #     f = "خوب"
        # if avg >= 5.0:
        #     f = "خیلی خوب"
        # if avg == 0:
        #     f = 'نظری داده نشده'

        # return float("%.1f" % round(my_avg, 2))
        if my_avg['rating__avg'] is None:
            return 0.0
        return my_avg['rating__avg']


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
