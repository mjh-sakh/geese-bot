import asyncio
import logging

from tests.test_config import TEST_BOT_CONFIG

import pytest
from telethon import TelegramClient
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
@pytest.mark.asyncio
async def bot(event_loop):
    logging.info('>> Creating bot.')
    bot = TelegramClient(
        None,
        TEST_BOT_CONFIG.api_id,
        TEST_BOT_CONFIG.api_hash,
        loop=event_loop,
    )
    bot.session.set_dc(3, TEST_BOT_CONFIG.test_server_ip, 443)
    await bot.start(bot_token=TEST_BOT_CONFIG.bot_token)
    # Issue a high level command to start receiving message
    # await bot.get_me()
    # # Fill the entity cache
    # await bot.get_dialogs()

    yield bot

    await bot.disconnect()
    await bot.disconnected


@pytest.fixture(scope="session")
@pytest.mark.asyncio
async def test_server_client(event_loop):
    logging.info('>> Creating client.')
    client = TelegramClient(
        StringSession(TEST_BOT_CONFIG.session_string),
        TEST_BOT_CONFIG.api_id,
        TEST_BOT_CONFIG.api_hash,
        loop=event_loop,
    )
    client.session.set_dc(3, TEST_BOT_CONFIG.test_server_ip, 443)
    await client.start()
    yield client
    await client.disconnect()
    await client.disconnected
