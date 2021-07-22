import asyncio
import logging

from pytest import mark
from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

from bot.bot_core import message_handler


@mark.asyncio
async def test_first(bot: TelegramClient, test_server_client: TelegramClient):
    bot.on(events.NewMessage)(message_handler)
    bot_data = await bot.get_me()
    async with test_server_client.conversation(bot_data.username) as conv:
        await conv.send_message('hello')
        resp: Message = await conv.get_response()
        assert 'Hi!' == resp.raw_text
