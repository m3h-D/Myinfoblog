from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Comments

# Create your views here.


def delete_comment(request, id):
    """function baraye pak kardane comment"""
    comment = get_object_or_404(Comments, id=id)
    if request.user == comment.user:
        comment.delete()
        messages.success(request, "کامنت شما با موفقیت حذف شد")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        # return redirect(comment.content_object.get_absolute_url())
    return None


def approve_comment(request, id):
    comment = get_object_or_404(Comments, id=id, approved=False)
    if request.user.is_staff or request.user.is_admin:
        comment.approved = True
        comment.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
