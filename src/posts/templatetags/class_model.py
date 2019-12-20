from django import template
from ..models import Post
from django.db.models import Count

register = template.Library()


@register.filter()
def class_model(model):
    return model.__class__.__name__


@register.simple_tag
def tags_side():
    """
    fahghat tag haye posta ro bar assasse unaei ke bishtarin
    view ro dashtan order mikone o 5 ta ye avval o bar migardoone
    """
    posts = Post.objects.filter(
        published=True
    ).values_list(
        'tags', flat=True
    ).annotate(
        count=Count("likes__likedislike")
    ).order_by('-count')

    the_tag = list()
    for tags in posts:
        for tag in tags:
            if tag in the_tag:  # age tage tekrari bud bikhialesh shoo
                continue
            the_tag.append(tag)
    # print('theeeeeeeeeeeeeee', the_tag)
    return the_tag[:5]
