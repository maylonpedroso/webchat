import asyncio

from django.test import TestCase

from bots import register, active_bots


class BotsRegisterTestCase(TestCase):

    def setUp(self) -> None:
        self.loop = asyncio.get_event_loop()

    def test_bot_is_registered_called_for_valid_message(self):
        @register.add('/test')
        async def test_bot(message):
            raise Exception('exception')

        self.assertIn('/test', active_bots)
        with self.assertRaisesMessage(Exception, 'exception'):
            self.loop.run_until_complete(active_bots['/test']('message'))
