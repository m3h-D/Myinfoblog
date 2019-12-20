from django.urls import path
from .views import home_page, panel_admin

urlpatterns = [
    path('', home_page, name='home-page'),
    path('panel-admin/', panel_admin, name='panel-admin'),

]
