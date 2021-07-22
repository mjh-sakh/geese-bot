from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from tests.test_config import TEST_BOT_CONFIG

client = TelegramClient(
    StringSession(),
    TEST_BOT_CONFIG.api_id,
    TEST_BOT_CONFIG.api_hash,
)
# client.session.set_dc(3, TEST_BOT_CONFIG.test_server_ip, 443)
client.start()
print("Your session string is:", client.session.save())
me = client.get_me()
print(me.stringify())
client.disconnect()
