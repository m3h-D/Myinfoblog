from django.urls import path
from .views import post_list, post_detail  # , post_like

urlpatterns = [
    path('', post_list, name='post-list'),
    path('<category_slug>/', post_list, name='category-list'),
    path('detail/<post_id>/<post_slug>/', post_detail, name='post-detail'),
    # path('likes/<post_id>/<post_slug>/', post_like, name='post-like'),
]
