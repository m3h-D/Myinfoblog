from django.urls import path
from .views import delete_comment, approve_comment


urlpatterns = [
    path('delete/<id>/', delete_comment, name='delete-comment'),
    path('approve/<id>/', approve_comment, name='approve-comment'),
]
