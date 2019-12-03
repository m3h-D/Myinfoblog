from django.urls import path
from .views import post_detail, post_search_view, post_list, update_post, delete_post  # , post_like

urlpatterns = [
    path('search/', post_search_view, name='post-search'),
    path('', post_list, name='post-list'),
    path('<category_slug>/', post_list, name='category-list'),
    path('update/<id>/<slug>/', update_post, name='post-update'),
    path('delete/<id>/<slug>/', delete_post, name='post-delete'),
    path('detail/<post_id>/<post_slug>/', post_detail, name='post-detail'),
    # path('likes/<post_id>/<post_slug>/', post_like, name='post-like'),
]
