from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.forms.models import model_to_dict

# Create your views here.
from .models import LikeDislike
from comments.models import Comments
from posts.models import Post

import json


def add_to_like(request, id, model_type):
    """Like kardane model ha barassase model_type ke to template
    be soorate str pass dade shude.
    """
    content_type = ContentType.objects.get(model=model_type)
    ModelType = content_type.model_class()
    model_type_qs = get_object_or_404(ModelType, id=id)
    # if request.is_ajax():
    #     qs = LikeDislike.objects.create_for_instance_model(
    #         instance=model_type_qs, request=request, likedislike='like')
    #     dicted_model = model_to_dict(qs)
    #     return HttpResponse(json.dumps(dicted_model))
    # else:
    LikeDislike.objects.create_for_instance_model(
        instance=model_type_qs, request=request, likedislike='like')
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def add_to_dislike(request, id, model_type):
    """Dislike kardane model ha barassase model_type ke to template
    be soorate str pass dade shude.
    """
    content_type = ContentType.objects.get(model=model_type)
    ModelType = content_type.model_class()
    model_type_qs = get_object_or_404(ModelType, id=id)
    # if request.is_ajax() and request.POST:
    #     likedislike_qs = LikeDislike.objects.create_for_instance_model(
    #         instance=model_type_qs, request=request, likedislike='dislike')
    #     return HttpResponse(json.dumps(likedislike_qs), conetnt_type='application/json')
    # else:
    LikeDislike.objects.create_for_instance_model(
        instance=model_type_qs, request=request, likedislike='dislike')

    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


# def add_to_like(request, comment_id=None, post_id=None):
#     """link e like kardane comment ha"""
#     if comment_id:
#         comment = get_object_or_404(Comments, id=comment_id)
#         comment.add_to_like_comment(request)
#         return redirect(comment.content_object.get_absolute_url())
#     if post_id:
#         post = get_object_or_404(Post, id=post_id)
#         post.add_to_like_post(request)
#         return HttpResponseRedirect(post.get_absolute_url())


# def add_to_dislike(request, id):
#     """linke like kardane post ha"""
#     comment = get_object_or_404(Comments, id=id)
#     comment.add_to_dislike_comment(request)
#     # content_type = ContentType.objects.get_for_model(Comments)
#     # try:
#     #     liked_or_not = comment.comment_like.get(request)
#     # except:
#     #     pass
#     # try:
#     #     # if comment.comment_like.get(request).liked == False:
#     #     disliked_comment = comment.comment_dislike.get(
#     #         request)
#     #     if disliked_comment.disliked == True:
#     #         disliked_comment.disliked = False
#     #         disliked_comment.delete()
#     #     else:
#     #         disliked_comment.disliked = True
#     #         disliked_comment.save()
#     #     # else:
#     #     #     disliked_comment.disliked = True
#     #     #     disliked_comment.save()
#     # except:

#     #     comment.comment_dislike.create(
#     #         request,
#     #         object_id=comment.id,
#     #         content_type=content_type,
#     #         disliked=True
#     #     )
#     #     try:
#     #         if liked_or_not.liked == True:
#     #             # liked_or_not.liked = False
#     #             liked_or_not.delete()
#     #     except:
#     #         pass

#     return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
