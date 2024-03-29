from django import forms
from django.shortcuts import redirect, reverse
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect

from .models import Comments
from .utils import uuid_generator


class CommentForm(forms.ModelForm):
    content_type = forms.CharField(widget=forms.HiddenInput, required=False)
    object_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    # contetn = forms.CharField(widget=forms.Textarea, label='محتوی')

    class Meta:
        model = Comments
        fields = ('content',)

    # def save(self, commit=True):
    #     comment = super(CommentForm, self).save(commit=False)
    #     comment.content = self.cleaned_data['content']
    #     if commit:
    #         comment.save()
    #         return comment


def comment_form(request, instance, parent_obj=None):
    """valid kardane comment form baraye har Model"""
    """try baraye ine ke motmaen shim data ei ke be parent_id dadan hatman int bashe (security)"""
    try:
        parent_id = int(request.POST.get('parent_id'))
    except:
        parent_id = None

    if parent_id:  # baraye peida kardan e parent e ye comment
        parent_qs = Comments.objects.filter(
            id=parent_id).order_by('timestamp')
        if parent_qs.exists():
            parent_obj = parent_qs.first()
    content_type = ContentType.objects.get_for_model(instance.__class__)
    comments_form = CommentForm(request.POST or None)
    # if request.method == "POST":
    if comments_form.is_valid():
        comments_form.instance.user = request.user
        comments_form.instance.content_type = content_type
        comments_form.instance.object_id = instance.id
        comments_form.instance.parent = parent_obj
        comments_form.instance.uuid = uuid_generator()
        comments_form.save()
        # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # else:
        return comments_form

    # form.instance.user = request.user
    # form.instance.content = form.cleaned_data['content']
    # form.instance.content_type = content_type
    # form.instance.object_id = instance.id
    # form.instance.parent = parent_obj
    # form.instance.uuid = uuid_generator(request)
    # form.save()
