from django.contrib.contenttypes.models import ContentType
from functools import wraps


PRIVATE_IPS_PREFIX = ('10.', '192.', '172.',)


def get_client_ip(request):
    """ip kasi ke dare request mide ro begir"""
    remote_address = request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        while (len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        if len(proxies) > 0:
            ip = proxies[0]

    return ip


def likedislike_manager(queryset, likedislike, request):
    """
    baraye behine kardane code(dry)
    """
    if queryset.likedislike == 'like' and likedislike == 'like':
        queryset.delete()
    elif queryset.likedislike == 'dislike' and likedislike == 'dislike':
        queryset.delete()
    elif queryset.likedislike == 'like' and likedislike == 'dislike':
        queryset.likedislike = 'dislike'
        if request.user.is_authenticated:
            queryset.user = request.user
        queryset.save()
    elif queryset.likedislike == 'dislike' and likedislike == 'like':
        queryset.likedislike = 'like'
        if request.user.is_authenticated:
            queryset.user = request.user
        queryset.save()
    return queryset


def get_or_create_auth_anon(ClassManager, instance, request, *args, **kwargs):
    ip_address = get_client_ip(request)
    # print('arge maaaaaaaaaaaan', kwargs, args)
    # my_filter = {
    #     kwargs.keys()[0]: kwargs.values()[0]
    # }
    content_type = ContentType.objects.get_for_model(
        instance.__class__)
    if request.user.is_authenticated:
        try:
            queryset = ClassManager.get(
                ip_address=ip_address,
                content_type=content_type,
                object_id=instance.id,
            )

        except:
            queryset = ClassManager.update_or_create(
                user=request.user,
                ip_address=ip_address,
                content_type=content_type,
                object_id=instance.id,
                content=instance.content,
                **kwargs
                # 'base'=kwargs.values()
            )
    elif request.user.is_anonymous:

        try:
            queryset = ClassManager.get(
                ip_address=ip_address,
                content_type=content_type,
                object_id=instance.id,
            )

        except:
            queryset = ClassManager.update_or_create(
                ip_address=ip_address,
                content_type=content_type,
                object_id=instance.id,
                content=instance.content,
                **kwargs
            )
    return queryset
