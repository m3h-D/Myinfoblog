from django.contrib import admin
from .models import LikeDislike
# Register your models here.


class LikeDislikeAdmin(admin.ModelAdmin):
    list_display = ('username_or_ip', 'likedislike',
                    'content_object', 'content_type', 'short_content')

    def username_or_ip(self, obj):
        try:
            return ("{}").format(obj.user.username)
        except:
            return ("{}").format(obj.ip_address)
    username_or_ip.short_description = 'کاربر'


admin.site.register(LikeDislike, LikeDislikeAdmin)
