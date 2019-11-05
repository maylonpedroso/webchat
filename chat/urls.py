from django.urls import path

from . import apps
from . import views

app_name = apps.ChatConfig.name

urlpatterns = [
    path('', views.room_view, name='index'),
]
