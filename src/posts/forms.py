from django import forms
from tinymce import TinyMCE

from .models import Post


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False
# class PostRateForm(forms.ModelForm):
#     class Meta:
#         model = Rate
#         fields = ("rating",)

# class SearchForm(forms.Form):
#     query = forms.CharField(
#         required=True)


class AddPostForm(forms.ModelForm):
    content = forms.CharField(label="افزونه", widget=TinyMCEWidget(
        attrs={'required': False, 'cols': 50, 'rows': 10}))

    class Meta:
        model = Post
        fields = ['title', 'image', 'category',
                  'content', 'tags', 'published', 'special']
