from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .utils import get_read_time, create_slug
from .models import Post, Category


@receiver(post_save, sender=Post)
def add_previous_post(sender, instance, created, *args, **kwargs):
    if created:
        instance.previous = instance.__class__.objects.filter(
            id__lt=instance.id).order_by('-id').first()
        instance.save()


@receiver(pre_save, sender=Post)
def create_read_time(sender, instance, *args, **kwargs):
    html_string = instance.content
    instance.read_time = get_read_time(html_string)
    # if not instance.previous:
    #     try:
    #         instance.previous = instance.__class__.objects.filter(
    #             id__lt=instance.id).order_by('-id').first()
    #     except:
    #         pass
    if not instance.slug:
        instance.slug = create_slug(instance)


@receiver(pre_save, sender=Category)
def category_slug_pre_populade(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
