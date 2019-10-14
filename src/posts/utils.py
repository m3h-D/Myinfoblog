import re
import datetime
import math
from django.utils.html import strip_tags
from django.utils.text import slugify


def word_counter(html_string):
    """tamam e kalamate dakhele file html o migire"""
    word_string = strip_tags(html_string)
    words_list = re.findall(r'\w+', word_string)
    count = len(words_list)
    return count


def get_read_time(html_string):
    """
    tedad kalamato taghsim bar 200 mikone ke yani
     200 kalame dar har daghighe.
     az math.ceil estefade shude ta be samte bala gerd kone adad o.
     """
    count = word_counter(html_string)
    read_time_min = math.ceil(count/80.0)
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(seconds=read_time_sec))
    read_time = str(datetime.timedelta(minutes=read_time_min))
    return read_time


def create_slug(instance, new_slug=None):
    """automatic barassasse title slug misaze.
        age slug vase ye posti mojood bud id post ham mizare kenaresh ta unique bashe
    """
    slug = slugify(("{}{}").format(instance.title, instance.id))
    if new_slug:
        slug = new_slug
    qs = instance.__class__.objects.filter(slug=slug)
    if qs.exists():
        new_slug = ("{}-{}").format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug
