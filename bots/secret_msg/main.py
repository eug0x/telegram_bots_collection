import asyncio
import logging
import uuid
import os
from collections import deque
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters import Command
from aiogram.types import (
    InlineQuery, 
    InlineQueryResultArticle, 
    InputTextMessageContent, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    CallbackQuery
)

load_dotenv()
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Storage
secret_messages = {}
query_queue = deque()

# Constants
MAX_MESSAGE_LENGTH = 193
CACHE_LIMIT = 1000

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = Router()

def manage_cache(msg_id, data):
    """Adds message to cache and removes oldest if limit reached."""
    secret_messages[msg_id] = data
    query_queue.append(msg_id)
    if len(secret_messages) > CACHE_LIMIT:
        oldest_id = query_queue.popleft()
        secret_messages.pop(oldest_id, None)

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Hi! I can send secret messages.\n"
        "Just use me in inline mode: @YourBot @username message\n\n"
        "1. Only the recipient can see the message. 🕵️‍♂️\n"
        "2. Character limit: 193. 🔤\n"
        "3. Message is deleted after being viewed. ❌"
    )

@router.inline_query()
async def inline_handler(inline_query: InlineQuery):
    query = inline_query.query.strip()
    
    if not query:
        result = InlineQueryResultArticle(
            id="instruction",
            title="How to send a message?",
            description="Type: @bot @username (your message)",
            input_message_content=InputTextMessageContent(
                message_text="To send a secret, use the format:\n@bot @username your_message"
            )
        )
        return await inline_query.answer([result], cache_time=0)

    if not query.startswith("@") or " " not in query:
        return

    try:
        parts = query.split(" ", 1)
        target_username = parts[0].replace("@", "").strip()
        message_text = parts[1].strip()

        if not message_text:
            return

        message_id = str(uuid.uuid4())
        
        if len(message_text) > MAX_MESSAGE_LENGTH:
            result = InlineQueryResultArticle(
                id="too_long",
                title="❌ Message too long",
                input_message_content=InputTextMessageContent(message_text="💥 The message is too long (max 193 chars).")
            )
        else:
            manage_cache(message_id, {"username": target_username, "message": message_text})
            
            kb = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="🔒 View Secret Message 🔒", callback_data=f"view_{message_id}")
            ]])
            
            result = InlineQueryResultArticle(
                id=message_id,
                title=f"✅ Secret for @{target_username}",
                input_message_content=InputTextMessageContent(
                    message_text=f"@{target_username}, you received a secret message! 🕵️‍♂️"
                ),
                reply_markup=kb
            )

        await inline_query.answer([result], cache_time=0, is_personal=True)
    except Exception as e:
        logger.error(f"Inline error: {e}")

@router.callback_query(F.data.startswith("view_"))
async def callback_handler(callback: CallbackQuery):
    message_id = callback.data.split("_", 1)[1]
    info = secret_messages.get(message_id)

    if not info:
        return await callback.answer("🔍 Message not found or already deleted.", show_alert=True)

    if callback.from_user.username != info["username"]:
        return await callback.answer(f"This secret is for @{info['username']} only! 😏", show_alert=True)

    await callback.answer(info["message"], show_alert=True)
    
    try:
        if callback.inline_message_id:
            await callback.bot.edit_message_reply_markup(inline_message_id=callback.inline_message_id, reply_markup=None)
        elif callback.message:
            await callback.message.edit_reply_markup(reply_markup=None)
    except Exception as e:
        logger.error(f"Markup edit error: {e}")

    secret_messages.pop(message_id, None)

@router.message(F.reply_to_message)
async def reply_handler(message: types.Message):
    target_user = message.reply_to_message.from_user.username
    if not target_user:
        return await message.reply("❌ Could not determine recipient's username.")

    msg_text = (message.text or "Empty message")[:MAX_MESSAGE_LENGTH]
    msg_id = str(uuid.uuid4())
    
    manage_cache(msg_id, {"username": target_user, "message": msg_text})

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="👀 View Message", callback_data=f"view_{msg_id}")
    ]])

    await message.answer(f"📬 @{target_user}, you received a secret message! 💌", reply_markup=kb)

async def main():
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")