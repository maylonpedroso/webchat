import asyncio

from django.test import TestCase

from chat.bots import register, notify_bots


class BotsRegisterTestCase(TestCase):

    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()

        @register('/test')
        async def test_bot(message):
            raise Exception('exception')

    def test_registered_bot_is_not_called_for_not_bot(self):
        self.loop.run_until_complete(notify_bots('message'))

    def test_registered_bot_is_not_called_for_another_bot(self):
        self.loop.run_until_complete(notify_bots('/bot message'))

    def test_registered_bot_is_called_for_valid_message(self):
        with self.assertRaisesMessage(Exception, 'exception'):
            self.loop.run_until_complete(notify_bots('/test message'))
