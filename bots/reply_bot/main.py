from telethon import TelegramClient, events
import asyncio
import time
import os
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
try:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    TARGET_USER_ID = int(os.getenv("TARGET_USER_ID"))
    # Fetching the reply text from .env
    AUTO_REPLY_TEXT = os.getenv("AUTO_REPLY_TEXT")
except (TypeError, ValueError):
    print("Error: Check API_ID, API_HASH, TARGET_USER_ID and AUTO_REPLY_TEXT in .env file")
    exit()

RESPONSE_DELAY = 5

last_incoming_event = {}
is_processing = asyncio.Lock()

# --- Client Initialization ---
client = TelegramClient('user', API_ID, API_HASH)

async def send_burnout_reply(sender_id):
    """Wait for delay and send the burnout message from .env."""
    if is_processing.locked():
        return
        
    async with is_processing:
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Waiting {RESPONSE_DELAY}s before replying...")
            await asyncio.sleep(RESPONSE_DELAY)

            event_to_reply = last_incoming_event.pop(sender_id, None)
            if event_to_reply is None:
                return

            await client.send_message(
                entity=sender_id,
                message=AUTO_REPLY_TEXT,
                reply_to=event_to_reply.id
            )
            
            print(f"[{time.strftime('%H:%M:%S')}] Reply sent to {sender_id}.")
            
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Error: {e}")

@client.on(events.NewMessage)
async def auto_reply_handler(event):
    """Handle messages only from the target user."""
    if event.out or event.sender_id != TARGET_USER_ID:
        return

    last_incoming_event[event.sender_id] = event

    if not is_processing.locked():
        print(f"[{time.strftime('%H:%M:%S')}] New message. Starting task...")
        asyncio.ensure_future(send_burnout_reply(event.sender_id))

async def main():
    await client.start()
    print(f'Userbot started. Monitoring User ID: {TARGET_USER_ID}')
    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())