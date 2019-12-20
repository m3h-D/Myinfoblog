from django import forms
from django.contrib.auth.models import User
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
        fields = ['author', 'title', 'image', 'category',
                  'content', 'tags', 'published', 'special']

        widgets = {
            'author': forms.HiddenInput,
        }

    # def __init__(self, *args, **kwargs):
    #     self.myuser = kwargs.pop('myuser', None)

    #     # print('userrrrrrrrrrrrrrr', self.myuser.email)
    #     super().__init__(*args, **kwargs)
    #     # print(self.fields['author'])
    #     try:
    #         # self.fields['author'].queryset = User.objects.filter(
    #         #     id=self.myuser.id)
    #         self.fields['author'] = self.myuser

    #     except:
    #         pass
