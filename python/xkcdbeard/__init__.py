from skybeard.beards import BeardChatHandler
from skybeard.utils import get_args
from skybeard.decorators import onerror
from skybeard.predicates import regex_predicate

import json

from pathlib import Path
from ftfy import fix_text
from aiohttp import ClientSession

# from . import xkcd


async def get_xkcd_json(number):
    async with ClientSession() as s:
        async with s.get("https://xkcd.com/{}/info.0.json".format(number)) as r:
            return json.loads(
                fix_text(
                    (await r.read()).decode("unicode_escape")))


class XkcdBeard(BeardChatHandler):

    __userhelp__ = """A simple xkcd beard."""

    __commands__ = [
        # command, callback coro, help text
        ("searchxkcd", 'search_xkcd', 'Echos command and args'),
        (regex_predicate("_test"), "_test_photo_sending", None)
    ]

    # __init__ is implicit

    @onerror
    async def search_xkcd(self, msg):
        args = get_args(msg)

        try:
            data = await get_xkcd_json(args[0])
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
