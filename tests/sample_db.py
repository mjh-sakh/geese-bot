import random
import string
from contextlib import AbstractContextManager
from datetime import datetime

import psycopg2
from psycopg2.sql import SQL, Identifier
from psycopg2.extensions import connection

from bot.config import BOT_CONFIG

CHARS = string.ascii_letters + string.punctuation
TEST_DB_NAME = "geese_test"


def random_string_generator(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))


def get_string(str_size: int) -> str:
    return random_string_generator(str_size, CHARS)


class DBConnection(AbstractContextManager):
    def __init__(self):
        pass

    def __enter__(self) -> connection:
        try:
            conn = psycopg2.connect(BOT_CONFIG.db_connect_string, dbname='postgres')
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(SQL('CREATE DATABASE {}').format(Identifier(TEST_DB_NAME)))
            cur.close()
            conn.close()
        except:
            pass
        conn = psycopg2.connect(BOT_CONFIG.db_connect_string, dbname=TEST_DB_NAME)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                      "id" serial NOT NULL,
                      PRIMARY KEY ("id"),
                      "sender_id" integer NOT NULL,
                      "message" text NOT NULL,
                      "date" timestamp NOT NULL,
                      "chat_id" integer NOT NULL
                        )
                    """
                    )
        cur.close()
        conn.close()
        self.conn = psycopg2.connect(BOT_CONFIG.db_connect_string, dbname=TEST_DB_NAME)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        try:
            conn = psycopg2.connect(BOT_CONFIG.db_connect_string, dbname='postgres')
            conn.autocommit = True
            cur = conn.cursor()
            cur.execute(SQL('DROP DATABASE {}').format(Identifier(TEST_DB_NAME)))
            cur.close()
            conn.close()
        except:
            print('Test database was not dropped')


def write_test_data():
    senders = {
        1: 'Mary',
        2: 'Vanya',
        3: 'Joe',
        4: 'Cindy',
    }
    with DBConnection() as conn:
        chat_id = 1
        cur = conn.cursor()
        for _ in range(100):
            sender_id = random.randint(1, len(senders))
            message = get_string(random.randint(20, 100))
            cur.execute(SQL("""
                        INSERT INTO {} (sender_id, message, date, chat_id)
                        VALUES (%s, %s, %s, %s)
                        """).format(Identifier('messages')),
                        (sender_id, message, datetime.now(), chat_id))
        conn.commit()
        cur.close()


write_test_data()
