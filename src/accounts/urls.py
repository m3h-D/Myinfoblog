from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,

)
from .views import load_towns, profile_edit, activate, login_view, register_view, logout_view


urlpatterns = [
    path('ajax-city-list/', load_towns, name='ajax-load-towns'),
    path('login/', login_view, name='login-view'),
    path('logout/', logout_view, name='logout-view'),
    path('register/', register_view, name='register-view'),
    path('profile/edit/', profile_edit, name='profile-edit'),
    # path('activate/<uidb64>/<token>/', activate, name='activate'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    path('password-change/', PasswordChangeView.as_view()),
    path('password-change/done/', PasswordChangeDoneView.as_view()),
    path('password_reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html'), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
         name='password_reset_complete'),
]
