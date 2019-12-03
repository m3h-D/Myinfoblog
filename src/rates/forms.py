from django import forms
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType

from .models import Rate


class RateForm(forms.ModelForm):
    """form i baraye modele Rate ke faqat 1 fieldesh dar dasrese"""
    class Meta:
        model = Rate
        fields = ('rating',)


def rate_form(request, instance, rates=None):
    content_type = ContentType.objects.get_for_model(instance.__class__)
    user = Rate.objects.filter_by_model(
        instance=instance).filter(user=request.user)
    rate_form = RateForm(request.POST or None)
    if request.method == 'POST':
        if rate_form.is_valid():
            if user.exists():
                pass
            else:
                rates = rate_form.save(commit=False)
                rates.user = request.user
                rates.content_type = content_type
                rates.object_id = instance.id
                rates.save()
                # return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
            return rates
