from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import BookMark

register = template.Library()


@register.simple_tag(takes_context=True)
def bookmark_btn_color(context, id, model_type):
    request = context['request']
    content_type = ContentType.objects.get(model=model_type)
    Model = content_type.model_class()
    model_qs = Model.objects.get(id=id)
    bookmark = BookMark.objects.filter_by_model(model_qs).first()
    try:
        if request.user.is_authenticated:
            if bookmark.user == request.user:
                return True
        else:
            pass
    except:
        return False
