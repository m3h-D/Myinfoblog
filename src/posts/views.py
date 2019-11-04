from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.serializers import serialize
from django.db.models import Count


from comments.models import Comments
from comments.forms import comment_form
from comments.utils import uuid_generator

from .models import Post, Category, Rate
# from .forms import PostRateForm
from rates.forms import rate_form
from likes.models import LikeDislike
from likes.utils import get_client_ip
from usertrackers.models import UserTracker
from usertrackers.signals import user_tracked_signal

import json


# Create your views here.
# def get_cat_count():
#     x = Post.objects.all().annotate(asd=Count('category__title'))
#     return x


def post_list(request, recommended=None, category_slug=None):
    """ function baseview e listi az post he publish shude"""
    posts = Post.objects.filter(published=True)

    for item in posts:
        recommended = item.recommended_posts(
            request=request)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=category, published=True)
    context = {'posts': posts,
               'recommended': recommended,
               }
    return render(request, 'posts/list.html', context)


def post_detail(request, post_id, post_slug, is_liked=False, user_has_rated=False, comment_forms=None, rate_forms=None):
    """
    function baseview e detail post ghabele dastresi ba id va slug
    gereftan e comment haye har post bar asase object_id va model e post

    """
    # category_count = get_cat_count()
    post = get_object_or_404(Post, id=post_id, slug=post_slug)
    """
    to inja ma dg az code zir estefade nemikonim
    va baraye har model say karim ye function e property
    besazim ke kheily behtare
    """
    # comments = Comments.objects.filter_by_model(instance=post)
    comments = post.comments
    """arg e avvali Sender e ke bayad classseshu bnvisim(ya Post mitunessim bnvisim)"""
    user_tracked_signal.send(
        post.__class__, instance=post, request=request)
    same_posts = Post.objects.filter(
        category__in=post.category.all()).exclude(id=post.id)
    ip_address = get_client_ip(request)

    if request.user.is_authenticated:

        comment_forms = comment_form(
            request=request, instance=post)  # dg niaz nist ke form o tu inja bebinim valid e ya na
        if not comment_forms == None:
            return redirect(post.get_absolute_url())

        rate_forms = rate_form(request=request, instance=post)
        if not rate_forms == None:
            return redirect(post.get_absolute_url())

        if post.rated_post.filter(user=request.user).exists():  # rating buttun
            user_has_rated = True
    message = messages.get_messages(request)

    context = {
        'post': post,
        'user_has_rated': user_has_rated,
        'comments': comments,
        'messages': message,
        'comment_form': comment_forms,
        'rate_form': rate_forms,
        'ip_address': ip_address,
        'same_posts': same_posts,
    }
    return render(request, 'posts/detail.html', context)
