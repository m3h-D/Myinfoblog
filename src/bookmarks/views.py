from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from .models import BookMark
from posts.models import Post

# Create your views here.


def bookmarked_list(request):
    bookmarks = BookMark.objects.filter(user=request.user)
    return render(request, 'bookmarks/list.html', {'bookmarks': bookmarks})


# def add_to_bookmark(request, post_id=None):
#     """Add/Remove kardane model be BookMark"""
#     if post_id:
#         post = get_object_or_404(Post, id=post_id)
#         post.add_to_bookmarked_post(user=request.user)
#         # return redirect(post.get_absolute_url())
#         return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def add_to_bookmark(request, id, model_type):
    """Add/Remove kardane model be BookMark"""
    content_type = ContentType.objects.get(model=model_type)
    # print("model type maaaaaaaaaaaaaaaaaaaan: ", content_type)
    ModelType = content_type.model_class()
    model_type_qs = get_object_or_404(ModelType, id=id)
    BookMark.objects.create_by_instance_model(
        instance=model_type_qs, user=request.user)

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def delete_from_bookmark(request, id):
    """bar assasse id e object e bookmark age user hamoon request.user bashe delete mikone"""
    content = get_object_or_404(BookMark, id=id)
    if content.user == request.user:
        content.delete()
    else:
        pass
    return redirect("bookmarks:bookmarked-list")
