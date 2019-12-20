"""advance_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/filebrowser/', site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('', include(('pages.urls', 'pages'), namespace='pages')),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('bookmarks/', include(('bookmarks.urls', 'bookmarks'), namespace='bookmarks')),
    path('posts/', include(('posts.urls', 'posts'), namespace='posts')),
    path('api/posts/', include(('posts.api.urls', 'posts-api'), namespace='posts-api')),
    path('comments/', include(('comments.urls', 'comments'), namespace='comments')),
    path('api/comments/', include(('comments.api.urls',
                                   'comments-api'), namespace='comments-api')),
    path('likes/', include(('likes.urls', 'likes'), namespace='likes')),
    path('api/likes/', include(('likes.api.urls', 'likes-api'), namespace='likes-api')),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL,
#                           document_root=settings.STATIC_ROOT)
