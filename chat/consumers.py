import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from chat import bots
from chat.models import ChatMessage, ChatRoom


class ChatConsumer(AsyncWebsocketConsumer):
    room_group_name: str = ''
    room: ChatRoom = None
    user: User = None

    async def connect(self) -> None:
        room_name: str = self.scope['url_route']['kwargs']['room_name']
        self.user: User = self.scope['user']
        if self.user.is_authenticated:
            self.room = await sync_to_async(ChatRoom.objects.get)(name=room_name)
            self.room_group_name = f'chat_{room_name}'
            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            message = json.loads(text_data).get('message', '')
            chat_message = ChatMessage(
                content=message, room=self.room, username=self.user.username
            )
            await sync_to_async(chat_message.save)()
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'datetime': chat_message.created_at.strftime("%m/%d/%Y, %H:%M:%S"),
                    'username': self.user.username,
                }
            )
            await bots.notify_bots(message)

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'datetime': event['datetime'],
            'username': event['username'],
        }))
