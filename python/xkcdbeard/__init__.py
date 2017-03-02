import asyncio

from skybeard.beards import BeardChatHandler
from skybeard.bearddbtable import BeardDBTable
from skybeard.utils import get_args
from skybeard.decorators import onerror
from skybeard.predicates import regex_predicate

import json

from pathlib import Path
from ftfy import fix_text
from aiohttp import ClientSession

# from . import xkcd


async def get_xkcd_json_data(number):
    async with ClientSession() as s:
        async with s.get("https://xkcd.com/{}/info.0.json".format(number)) as r:
            # thedata = json.loads(fix_text((await r.read()).decode("unicode_escape")))
            # import pdb; pdb.set_trace()
            # return thedata
            return await r.text()


async def get_xkcd_json(number=None, data=None):
    assert not (number is not None and data is not None)
    if number is not None:
        data = await get_xkcd_json_data(number)

    return json.loads(fix_text(data))


class XkcdBeard(BeardChatHandler):

    __userhelp__ = """A simple xkcd beard."""

    __commands__ = [
        # command, callback coro, help text
        ("searchxkcd", 'search_xkcd', 'Echos command and args'),
        (regex_predicate("_test"), "_test_photo_sending", None)
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        asyncio.ensure_future(self._update_xkcd_cache())

    @classmethod
    async def _update_xkcd_cache(cls):
        # Find where to start from
        with cls.xkcd_cache_table as table:
            last_comic = max([x['num'] for x in table.all()])
        for i in reversed(range(1, last_comic+1)):
            with cls.xkcd_cache_table as table:
                entry = table.find_one(num=i)
            if not entry:
                data = await get_xkcd_json(i)
                with cls.xkcd_cache_table as table:
                    table.insert(data)

    @classmethod
    async def _get_xkcd_json_from_cache(cls, num):
        with cls.xkcd_cache_table as table:
            return table.find_one(num=num)

    @onerror
    async def search_xkcd(self, msg):
        args = get_args(msg)

        try:
            await self.sender.sendChatAction('upload_photo')
            data = await self._get_xkcd_json_from_cache(args[0])
            await self.sender.sendPhoto(data['img'],
                                        caption=data['alt'])
        except IndexError:
            self.sender.sendMessage("No issue number provided?")
            return

    @onerror
    async def _test_photo_sending(self, msg):
        path = Path(
            "/home/nasfarley88/git/skybeard-2/xkcd_archive/301/Limerick.png")
        await self.sender.sendPhoto(path.open("rb"))


XkcdBeard.xkcd_cache_table = BeardDBTable(XkcdBeard, "xkcd_cache")
