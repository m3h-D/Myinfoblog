from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth import get_user_model, authenticate

from .models import Profile, City, Town


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=120, label="نام کاربری")
    password = forms.CharField(
        max_length=120, label="رمز عبور", widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("چنین مشخصاتی وجود ندارد")
            elif user.is_active == False:
                raise forms.ValidationError("اکانت شما غیر فعال است")
            return super(LoginForm, self).clean(*args, **kwargs)


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="نام کاربری")
    first_name = forms.CharField(label="نام", required=False)
    last_name = forms.CharField(label="نام خانوادگی", required=False)
    email = forms.EmailField(label="ایمیل", required=True)
    email2 = forms.EmailField(label="تکرار ایمیل")
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="تکرار رمز عبور", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'email2', 'password1', 'password2')

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email and email2 and email != email2:
            raise forms.ValidationError("ایمیل ها برابر نیستند")
        email_exists = User.objects.filter(email=email)
        if email_exists.exists():
            raise forms.ValidationError("این ایمیل قبلا استفاده شده")
        return super(RegisterForm, self).clean(*args, **kwargs)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            # 'first_name',
            # 'last_name',
            'username',
            'email',
        ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'bio',
            'phone',
            'city',
            'town',
            'address',
            'image',
            'post_code'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['town'].queryset = Town.objects.none()
        # hess mikonam khat e bala yani Town.objects.all() = None (list e khali)

        if 'city' in self.data:
            try:
                city = int(self.data.get('city'))
                self.fields['town'].queryset = Town.objects.filter(
                    city=city).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # mishe elif e paein o nanevesht chun bala be soorate default town none tarif shude
        elif not self.instance.pk:  # fek konam manzoore in khat ineke age city nabud ye list e khali az town bargardoon
            self.fields['town'].queryset = self.instance.city.town.order_by(
                'name')  # dar vaghe in khat , khat 2 e __init__ e ke None barmigashtund inja mige dar soorati ke city None bud
            # -------- ya ---------------------------------
            # self.fields['town'].queryset = []


# class ProfileForm(forms.ModelForm):

#     class Meta:
#         model = Profile
#         fields = ("__all__")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['town'].queryset = Town.objects.none()

#         if 'country' in self.data:
#             try:
#                 city = int(self.data.get('city'))
#                 self.fields['town'].queryset = Town.objects.filter(
#                     city=city).order_by('name')
#             except (ValueError, TypeError):
#                 pass  # invalid input from the client; ignore and fallback to empty City queryset
#         elif self.instance.pk:
#             self.fields['town'].queryset = self.instance.city.town.order_by(
#                 'name')
