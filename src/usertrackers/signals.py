from django.dispatch import receiver, Signal
from .models import UserTracker
from django.contrib.contenttypes.models import ContentType
from likes.utils import get_client_ip


user_tracked_signal = Signal(providing_args=['instance', 'request'])


# @receiver(sender=user_tracked_signal)
def user_tracked_reciver(sender, instance, request, *args, **kwargs):
    """signale balaro migire o bar assasse vorodi hash ye UserTracker baraye user misaze"""
    ip_address = get_client_ip(request)
    if request.user.is_authenticated:
        UserTracker.objects.create(user=request.user,
                                   ip_address=ip_address,
                                   object_id=instance.id,
                                   content_type=ContentType.objects.get_for_model(
                                       sender),
                                   content_object=instance,
                                   viewed_count=0)
    elif request.user.is_anonymous:
        UserTracker.objects.create(ip_address=ip_address,
                                   object_id=instance.id,
                                   content_type=ContentType.objects.get_for_model(
                                       sender),
                                   content_object=instance,
                                   viewed_count=0)


user_tracked_signal.connect(user_tracked_reciver)
