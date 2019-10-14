from django.urls import path
from .views import add_to_bookmark, bookmarked_list

urlpatterns = [
    path('', bookmarked_list, name='bookmarked-list'),
    path('add/<int:post_id>', add_to_bookmark, name='add-to-bookmarke'),
]
