"""Core module to start and run bot."""

import logging
from datetime import datetime
from functools import partial

import psycopg2
from telethon import TelegramClient, events

from bot.config import BOT_CONFIG


def run():
    conn = psycopg2.connect(BOT_CONFIG.db_connect_string, dbname=BOT_CONFIG.db_name)
    bot = TelegramClient(BOT_CONFIG.session, BOT_CONFIG.api_id, BOT_CONFIG.api_hash)
    message_handler_with_db = partial(message_handler, conn)
    bot.on(events.NewMessage)(message_handler_with_db)
    bot.start(bot_token=BOT_CONFIG.bot_token)
    bot.run_until_disconnected()
    conn.close()


async def message_handler(db_conn, event):
    # chat = await event.get_chat()
    # await bot.download_profile_photo(sender)
    chat_id = event.chat_id
    sender_id = event.sender_id
    text = event.raw_text
    logging.info(f'incoming message: {text}')
    logging.info(f'chat_id: {chat_id}')
    logging.info(f'sender_id: {sender_id}')

    cur = db_conn.cursor()
    cur.execute("""
                INSERT INTO messages (sender_id, chat_id, message, date) 
                VALUES (%s, %s, %s, %s)
                """,
                (sender_id, chat_id, text, datetime.now()))
    cur.close()
    db_conn.commit()

    if text.lower() == 'hello':
        await event.reply('Hi!')

    if text.lower() == r'\activity':
        cur = db_conn.cursor()
        cur.execute("""
                    SELECT name, COUNT(message) 
                    FROM messages JOIN users ON messages.sender_id = users.sender_id 
                    GROUP BY name
                    """)
        data = cur.fetchall()
        cur.close()
        await event.reply(f'{data}')
