import asyncio

from channels.layers import get_channel_layer
from channels_redis.core import RedisChannelLayer
from django.core.management.base import BaseCommand

from bots import active_bots
from chat.models import ChatRoom


loop = asyncio.get_event_loop()


class Command(BaseCommand):
    help = 'Run all registered bots'
    channel_layer: RedisChannelLayer = get_channel_layer()

    def handle(self, *args, **options):
        loop.run_until_complete(asyncio.gather(
            *(self.group_processor(f'chat_{room.name}') for room in ChatRoom.objects.all())
        ))
        self.stderr.write(self.style.WARNING(f'There are no rooms available'))

    async def group_processor(self, group_name):
        self.stdout.write(self.style.SUCCESS(f'Start listening to "{group_name}" room'))

        channel_name = await self.channel_layer.new_channel()
        await self.channel_layer.group_add(group_name, channel_name)

        while True:
            self.stdout.write(
                self.style.SUCCESS(f'Waiting for message in "{channel_name}" channel')
            )
            message = await self.channel_layer.receive(channel_name)
            if message.get('type') == 'chat_message':
                try:
                    name, value = message.get('message', '').split('=', maxsplit=2)
                    result = await active_bots[name](value)
                except (ValueError, KeyError):
                    pass
                else:
                    await self.channel_layer.group_send(group_name, result)
