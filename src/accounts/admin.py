from django.contrib import admin
from .models import Profile, Town, City

# from .forms import UserChangeForm
# from .models import User


# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserChangeForm
#     add_form = UserCreationForm

#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('email', 'phone', 'is_admin')
#     list_filter = ('is_admin',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('phone',)}),
#         ('Permissions', {'fields': ('is_admin',)}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'phone', 'password1', 'password2')}
#         ),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()

# # Now register the new UserAdmin...
# admin.site.register(MyUser, UserAdmin)
# # ... and, since we're not using Django's built-in permissions,
# # unregister the Group model from admin.
# admin.site.unregister(Group)


admin.site.register(Profile)
admin.site.register(Town)
admin.site.register(City)

# Register your models here.
