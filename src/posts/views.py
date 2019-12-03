from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.views.decorators import staff_member_required
from django.core.serializers import serialize
from django.db.models import Count, Q
from django.http import HttpResponseRedirect


from comments.models import Comments
from comments.forms import comment_form
from comments.utils import uuid_generator

from .models import Post, Category, Rate
from .forms import AddPostForm
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

def post_search_view(request):
    # results = list()
    # query = None
    # form = SearchForm()
    # if 'query' in request.GET:
    # form = SearchForm(request.GET)
    # if form.is_valid():
    query = request.GET.get('results')
    results = Post.objects.filter(published=True)
    if 'results' in request.GET:
        # query = form.cleaned_data['query']
        search_vector = SearchVector(
            'title', 'content', 'tags')
        search_query = SearchQuery(query)
        # results = Post.objects.annotate(search=SearchVector(
        #     'title',),).filter(search=query)
        results = Post.objects.annotate(search=search_vector, rank=SearchRank(
            search_vector, search_query),).filter(search=search_query).order_by("-rank")
    # context = {
    #     'query': query,
    #     'results': results}
    return render(request, 'posts/mysearch.html', {'query': query, 'results': results})


def post_list(request, category_slug=None):
    """ function baseview e listi az post he publish shude"""
    posts = Post.objects.filter(published=True)

    recommended = None
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


def post_detail(request, post_id, post_slug, user_has_rated=False):
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
    try:
        same_posts = Post.objects.filter(
            tags__overlap=post.tags).exclude(id=post.id)
    except:
        same_posts = Post.objects.filter(
            category__in=post.category.all()).distinct().exclude(id=post.id)
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


@staff_member_required
def update_post(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    categories = Category.objects.all()

    update_form = AddPostForm(request.POST or None,
                              request.FILES or None, instance=post)
    if request.method == 'POST':
        if update_form.is_valid():
            update_form.instance.author = request.user
            update_form.save()
            return redirect(post.get_absolute_url())
    # return render(request, 'panelAdmin.html', {'update_form': update_form})
    return render(request, 'posts/update_post.html', {'update_form': update_form, 'categories': categories})


@staff_member_required
def delete_post(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    post.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@staff_member_required
def create_post(request):
    form = AddPostForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect(reverse("posts:post-detail", kwargs={'post_id': form.instance.id,
                                                                 'post_slug': form.instance.slug}))
    return form
