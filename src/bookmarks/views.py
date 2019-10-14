from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import BookMark
from posts.models import Post

# Create your views here.


def bookmarked_list(request):
    bookmarks = BookMark.objects.filter(user=request.user)
    return render(request, 'bookmarks/list.html', {'bookmarks': bookmarks})


def add_to_bookmark(request, post_id=None):
    """Add/Remove kardane model be BookMark"""
    if post_id:
        post = get_object_or_404(Post, id=post_id)
        post.add_to_bookmarked_post(user=request.user)
        # return redirect(post.get_absolute_url())
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
