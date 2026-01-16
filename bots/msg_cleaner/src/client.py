from telethon import TelegramClient
from src.config import API_ID, API_HASH, SESSION_NAME

async def get_client():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()
    return client