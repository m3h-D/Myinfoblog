from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm, LoginForm, RegisterForm
from .models import Town
# --------------------activation----------------
from .tasks import send_confirmation_email
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from urllib.parse import urlsplit


User = get_user_model()
# Create your views here.


def login_view(request):
    """faqat uniei ke login nakardan mitunan login konan"""
    next = request.GET.get('next')
    if request.user.is_authenticated:
        if next:
            return redirect(next)
        return redirect('accounts:profile-edit')
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        else:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    return render(request, 'accounts/login.html', {"form": form})


@login_required
def logout_view(request, *args, **kwargs):
    logout(request, *args, **kwargs)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register_view(request):
    """
    faghat uni ke login nakarde mitune register kone
    amma accountesh ghyre faal mishe va ye email barash mifreste
    ta vaghti un email o active nakone is_active = False
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            protocol = urlsplit(request.build_absolute_uri(None)).scheme
            current_site = get_current_site(request)
            message = render_to_string('accounts/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': protocol,
            })
            to_email = form.cleaned_data.get('email')
            send_confirmation_email.delay(message, to_email)
            return HttpResponse('لینک فعال سازی برای ایمیل شما ارسال شد')

    return render(request, 'accounts/register.html', {"form": form})


def activate(request, uidb64, token):
    """
    dar soorate mojud budane user id e user o decode mikone va check mikone 
    token ro ham hamrahe hamoon id e user check mikone
    age dorost bashe user is_active = True va login mishe 
    age na payame link na mootabar ast mide  
    """
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('pages:home-page')
        # return HttpResponse('اکانت شما فعال شد حال می توانید وارد شوید')
    else:
        return HttpResponse('لینک نا معتبر است.')


@login_required
def profile_edit(request):
    """ye form az tarkibe User o Profile"""
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # messages.success(request, f'پروفایل شما بروز رسانی شد')s
            return redirect('posts:post-list')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,

    }
    return render(request, 'accounts/profile_edit.html', context)


def load_towns(request):
    """
    city ro az form e edit-profile migire baad
    to ye html dg bessorate ajax field town o update mikone

    """
    city = request.GET.get('city')
    towns = Town.objects.filter(city=city)
    return render(request, 'accounts/city_town_list.html', {'towns': towns})
