import asyncio
import unittest
from hypothesis import given, strategies, note

import python.xkcdbeard as xkcdbeard


class TestGetXkcdJson(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    @given(num=strategies.integers(1, 1700))
    def test_get_xkcd_json_data(self, num):
        async def go():
            await xkcdbeard.get_xkcd_json_data(num)
        self.loop.run_until_complete(go())

    @given(num=strategies.integers(1, 1700))
    def test_get_xkcd_json(self, num):
        async def go():
            x = await xkcdbeard.get_xkcd_json_data(num)
            note(x)
            await xkcdbeard.get_xkcd_json(data=x)
        self.loop.run_until_complete(go())
