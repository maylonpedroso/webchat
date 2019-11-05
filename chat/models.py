from django.conf import settings
from django.db import models


class ChatRoom(models.Model):
    name = models.CharField(max_length=15, unique=True)


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    content = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now=True)
