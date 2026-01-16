import asyncio
import logging
import os
import difflib
import random
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError 
from telethon.tl.types import MessageMediaDocument, DocumentAttributeAudio
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID"))
DESTINATION_CHANNEL_ID = int(os.getenv("DESTINATION_CHANNEL_ID"))
LAST_PROCESSED_ID = 4969 # Resume from this message ID

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants & Filters
MIN_SIZE = 1024 * 1024 # 1 MB
MAX_SIZE = 40 * 1024 * 1024 # 40 MB
ALLOWED_MIMES = ['audio/mpeg', 'audio/mp3']
SENT_TITLES = set()
SIMILARITY_THRESHOLD = 0.90
TITLE_BLACKLIST = {'unknown', 'track', 'audio', 'неизвестный'}

# Anti-Flood settings
TRANSFER_COUNT = 0
TRANSFER_LIMIT = 500
LONG_PAUSE = 120 # 2 minutes pause after limit reached
FIXED_DELAY = 1.0 # 1 second between messages

def clean_title(title: str, performer: str) -> str:
    return f"{performer} {title}".strip().lower()

def is_duplicate(current_title_clean: str) -> bool:
    if not current_title_clean:
        return False
    
    if any(word in current_title_clean for word in TITLE_BLACKLIST):
        return True

    for sent_title in SENT_TITLES:
        if difflib.SequenceMatcher(None, current_title_clean, sent_title).ratio() >= SIMILARITY_THRESHOLD:
            return True
    return False

async def transfer_message(client, message):
    global TRANSFER_COUNT
    if not (message.media and isinstance(message.media, MessageMediaDocument)):
        return

    doc = message.media.document
    audio_attr = next((a for a in doc.attributes if isinstance(a, DocumentAttributeAudio)), None)

    if audio_attr:
        if doc.mime_type not in ALLOWED_MIMES:
            return

        title = getattr(audio_attr, 'title', '') or ''
        performer = getattr(audio_attr, 'performer', 'Unknown') or ''
        
        if not title and not performer:
            return

        if not (MIN_SIZE <= doc.size <= MAX_SIZE):
            return

        cleaned = clean_title(title, performer)
        if is_duplicate(cleaned):
            return

        SENT_TITLES.add(cleaned)

        try:
            await client.send_file(DESTINATION_CHANNEL_ID, message, caption='', silent=True)
            logging.info(f"✅ Forwarded: {performer} - {title}")
            TRANSFER_COUNT += 1
        except FloodWaitError as e:
            logging.critical(f"🚨 Flood Wait: {e.seconds}s. Sleeping...")
            await asyncio.sleep(e.seconds)
            return
        except Exception as e:
            logging.error(f"❌ Error: {e}")

        await asyncio.sleep(FIXED_DELAY)

        if TRANSFER_COUNT >= TRANSFER_LIMIT:
            logging.warning(f"Limit reached. Resting for {LONG_PAUSE}s...")
            TRANSFER_COUNT = 0
            await asyncio.sleep(LONG_PAUSE)

async def main():
    client = TelegramClient('forwarder_session', API_ID, API_HASH)
    await client.start()
    logging.info("Forwarder Bot Started!")

    # 1. Process History
    async for message in client.iter_messages(SOURCE_CHANNEL_ID, reverse=True, min_id=LAST_PROCESSED_ID):
        await transfer_message(client, message)

    # 2. Listen for New Messages
    @client.on(events.NewMessage(chats=SOURCE_CHANNEL_ID, incoming=True))
    async def handler(event):
        await transfer_message(client, event.message)

    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())