from django import forms
from django.shortcuts import redirect
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
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment_form = form.save(commit=False)
        comment_form.user = request.user
        comment_form.content_type = content_type
        comment_form.object_id = instance.id
        comment_form.parent = parent_obj
        comment_form.uuid = uuid_generator()
        comment_form.save()
        return comment_form

    # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # form.instance.user = request.user
    # form.instance.content = form.cleaned_data['content']
    # form.instance.content_type = content_type
    # form.instance.object_id = instance.id
    # form.instance.parent = parent_obj
    # form.instance.uuid = uuid_generator(request)
    # form.save()
    # return HttpResponseRedirect('')
