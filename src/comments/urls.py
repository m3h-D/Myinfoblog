from django.urls import path
from .views import delete_comment


urlpatterns = [
    path('delete/<id>/', delete_comment, name='delete-comment'),
]
