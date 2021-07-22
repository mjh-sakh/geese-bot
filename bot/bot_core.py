"""Core module to start and run bot."""

import logging

from telethon import TelegramClient, events

from bot.config import BOT_CONFIG


def run():
    bot = TelegramClient(BOT_CONFIG.session, BOT_CONFIG.api_id, BOT_CONFIG.api_hash)
    bot.on(events.NewMessage)(message_handler)
    bot.start(bot_token=BOT_CONFIG.bot_token)
    bot.run_until_disconnected()


async def message_handler(event):
    # chat = await event.get_chat()
    # await bot.download_profile_photo(sender)
    chat_id = event.chat_id
    sender_id = event.sender_id
    text = event.raw_text
    logging.info(f'incoming message: {text}')
    logging.info(f'chat_id: {chat_id}')
    logging.info(f'sender_id: {sender_id}')
    if text.lower() == 'hello':
        await event.reply('Hi!')
