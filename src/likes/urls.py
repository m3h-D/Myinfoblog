from django.urls import path
from.views import add_to_dislike, add_to_like

urlpatterns = [
    # path('like/<int:comment_id>/comment/',
    #      add_to_like, name='add-to-like-comment'),
    # path('like/<post_id>/post/', add_to_like, name='add-to-like-post'),
    path('dislike/<int:id>/<model_type>/',
         add_to_dislike, name='add-to-dislike'),
    path('like/<int:id>/<model_type>/', add_to_like, name='add-to-like'),
]
