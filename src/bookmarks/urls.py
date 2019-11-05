from django.urls import path
from .views import add_to_bookmark, bookmarked_list, delete_from_bookmark

urlpatterns = [
    path('', bookmarked_list, name='bookmarked-list'),
    path('delete/<int:id>/', delete_from_bookmark, name='delete-from-bookmark'),
    # path('add/<int:post_id>', add_to_bookmark, name='add-to-bookmarke'),
    path('add/<int:id>/<model_type>/',
         add_to_bookmark, name='add-to-bookmarke'),
]
