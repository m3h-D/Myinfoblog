from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from likes.utils import get_client_ip

# Create your models here.

User = get_user_model()


class UserTrackerManager(models.Manager):

    def filter_by_model(self, instance):
        """bar assasse model filter mikone"""
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        queryset = super(UserTrackerManager, self).filter(
            content_type=content_type, object_id=object_id)
        return queryset

    def recommended_list(self, request, instance):
        """ye recommended list bar assasse category va session"""
        if request.user.is_authenticated:
            viewed_item = self.filter_by_model(
                instance=instance).filter(user=request.user)
        elif request.user.is_anonymous:
            ip_address = get_client_ip(request)
            viewed_item = self.filter_by_model(
                instance=instance).filter(user__isnull=True, ip_address=ip_address)
        same_category = list()
        for item in viewed_item:
            # category e post haei ke user dide
            same_category = item.content_object.category.values_list(
                'id', flat=True)

        queryset = instance.__class__.objects.filter(
            category__id__in=same_category)
        # .annotate(count=models.Count('likes__likedislike')).order_by('-count')[:3]
        # self.same_cate += list(queryset.values_list('pk', flat=True))
        try:
            """ye session e listi misaze ke Model o bar assasse category e bala filter mikone"""
            request.session['same_categories'] += list(queryset.values_list(
                'pk', flat=True))  # bareye in az values_list o pk estefade kardim ke dg niaz be serialize kardan nabshe

        except:
            # request.session['same_categories'] = list()
            request.session['same_categories'] = list(
                queryset.values_list('pk', flat=True))

        # same_item = instance.__class__.objects.filter(
        #     pk__in=self.same_cate)

        # sessioni ke bala sakhte shu o mirize to ye moteghayer o bar migardoone
        same_item = instance.__class__.objects.filter(
            pk__in=request.session.get('same_categories'))

        return same_item


class UserTracker(models.Model):
    """track kardane karbar (ke kodom safe ha ro karbar dide)"""
    user = models.ForeignKey(User, related_name='usertracker',
                             on_delete=models.CASCADE, blank=True, null=True, verbose_name='کاربر')
    ip_address = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='ای پی')
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    viewed_count = models.PositiveIntegerField(verbose_name='دفعات')
    viewed_on = models.DateTimeField(auto_now_add=True)

    objects = UserTrackerManager()

    class Meta:
        """order kardan bar assasse tarikhe view shude"""
        ordering = ('-viewed_on',)
        verbose_name = "دیده شده توسط کاربر"
        verbose_name_plural = "دیده شده توسط کاربر ها"

    def __str__(self):
        try:
            return ("{} در تاریخ {} - {} را دیده").format(self.user.username, self.viewed_on, self.content_object.title)
        except:
            return ("{} در تاریخ {} - {} را دیده").format(self.ip_address, self.viewed_on, self.content_object.title)
        finally:
            return ("{} در تاریخ {} -  را دیده").format(self.ip_address, self.viewed_on)
