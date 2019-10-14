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
        try:
            user_tracker = UserTracker.objects.get(user=request.user, ip_address=ip_address, object_id=instance.id, content_type=ContentType.objects.get_for_model(
                sender))
            user_tracker.viewed_count += 1
            user_tracker.save()
        except:
            UserTracker.objects.create(user=request.user,
                                       ip_address=ip_address,
                                       object_id=instance.id,
                                       content_type=ContentType.objects.get_for_model(
                                           sender),
                                       content_object=instance,
                                       viewed_count=1)
    elif request.user.is_anonymous:
        try:
            user_tracker = UserTracker.objects.get(ip_address=ip_address, object_id=instance.id, content_type=ContentType.objects.get_for_model(
                sender))
            user_tracker.viewed_count += 1
            user_tracker.save()
        except:
            UserTracker.objects.create(
                ip_address=ip_address,
                object_id=instance.id,
                content_type=ContentType.objects.get_for_model(
                    sender),
                content_object=instance,
                viewed_count=1)


user_tracked_signal.connect(user_tracked_reciver)
