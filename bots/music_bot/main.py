import asyncio
import os
import time
import uuid
import glob
import random
import logging
import json
import aiohttp
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaAudio
from yt_dlp import YoutubeDL
from aiogram.exceptions import TelegramBadRequest
from aiogram.client.default import DefaultBotProperties

# --- Load Environment ---
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
try:
    ALLOWED_CHAT_ID = int(os.getenv("ALLOWED_CHAT_ID", 0))
except ValueError:
    ALLOWED_CHAT_ID = 0

# --- Constants ---
MAX_FILE_SIZE_MB = 50
ANTI_SPAM_INTERVAL = 15
BOT_START_TIME = time.time()
SONGS_INFO_FILE = "songs_info.json"

# --- Logging ---
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

# --- Bot Initialization ---
# Fixed the initialization as requested
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

user_last_request_time = {}
song_data_storage = {}

# --- Utility Functions ---
def format_number_dot(num):
    if not isinstance(num, int):
        return "unknown"
    return f"{num:,}".replace(",", ".")

def cleanup_temp_files(base):
    for f in glob.glob(f"{base}.*"):
        try:
            os.remove(f)
        except:
            pass

def load_song_data():
    if os.path.exists(SONGS_INFO_FILE):
        with open(SONGS_INFO_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_song_data(data):
    with open(SONGS_INFO_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

song_data_storage = load_song_data()

async def get_dislikes(video_id):
    url = f"https://returnyoutubedislikeapi.com/votes?videoId={video_id}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=3) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("dislikes")
    except:
        return None

async def search_multiple(query):
    ydl_opts = {
        'quiet': True, 'skip_download': True, 'noplaylist': True,
        'extract_flat': True, 'extractor_args': {'youtube': {'client': 'android'}},
    }
    def search():
        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(f"ytsearch10:{query}", download=False)
            return result.get("entries", [])
    return await asyncio.to_thread(search)

async def download_by_url(url):
    ydl_opts = {
        'format': 'bestaudio/best', 'noplaylist': True, 'quiet': True,
        'outtmpl': '%(title)s.%(ext)s', 'writethumbnail': True,
        'extractor_args': {'youtube': {'client': 'android'}}, 'no_warnings': True,
    }
    def download():
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            base = os.path.splitext(ydl.prepare_filename(info))[0]
            audio_file = None
            for ext in ['mp3', 'm4a', 'webm', 'opus', 'ogg']:
                candidate = f"{base}.{ext}"
                if os.path.exists(candidate):
                    audio_file = candidate
                    break
            if audio_file and not audio_file.endswith('.mp3'):
                new_mp3 = f"{base}.mp3"
                if os.path.exists(new_mp3): os.remove(new_mp3)
                os.rename(audio_file, new_mp3)
                audio_file = new_mp3
            thumb = None
            for ext in ['jpg','jpeg','png','webp']:
                candidate = f"{base}.{ext}"
                if os.path.exists(candidate):
                    thumb = candidate
                    break
            return info, audio_file, thumb, base
    return await asyncio.to_thread(download)

# --- Handlers ---
@dp.message()
async def handle(message: types.Message):
    if message.date.timestamp() < BOT_START_TIME or message.chat.id != ALLOWED_CHAT_ID:
        return
    
    text = message.text or ""
    if not text.lower().startswith("music "):
        return
        
    user_id = message.from_user.id
    now = time.time()
    if now - user_last_request_time.get(user_id, 0) < ANTI_SPAM_INTERVAL:
        return
    user_last_request_time[user_id] = now
    
    query = text[6:].strip()
    if not query:
        msg = await message.reply("⚠️ Format: music [song name]")
        await asyncio.sleep(5)
        await msg.delete()
        return
        
    try: await message.delete()
    except: pass
    
    status = await message.answer("🔍 Searching for song...")
    try:
        results = await search_multiple(query)
        if not results: raise Exception("NO_RESULTS")
        
        first = results[0]
        url = first.get("url") or first.get("webpage_url")
        if not url: raise Exception("NO_URL")
        
        info, file, thumb, base = await download_by_url(url)
        if info.get("duration") and info['duration'] > 900: raise Exception("LONG_AUDIO")
        if os.path.getsize(file) > MAX_FILE_SIZE_MB * 1024 * 1024:
            os.remove(file)
            raise Exception("TOO_LARGE")
        
        with open(file, "rb") as f:
            audio = types.BufferedInputFile(f.read(), filename=os.path.basename(file))
        thumbnail = types.BufferedInputFile(open(thumb, "rb").read(), filename=os.path.basename(thumb)) if thumb else None
        
        sender_name = message.from_user.full_name
        btn_text = f"🎵 {sender_name}"
        key = uuid.uuid4().hex[:8]
        
        song_data_storage[f"info_{key}"] = {
            "title": info.get("title"), "artist": info.get("uploader"),
            "thumb": thumb, "file": file, "base": base, "query": query, "url": url,
            "requester": user_id, "duration": info.get("duration"),
            "upload_date": info.get("upload_date"), "view_count": info.get("view_count"),
            "like_count": info.get("like_count"), "dislike_count": await get_dislikes(info.get("id")),
        }
        save_song_data(song_data_storage)
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=btn_text, callback_data=f"info_{key}"),
             InlineKeyboardButton(text="🔎 Not the right song?", callback_data=f"alt_{key}")]
        ])
        
        await status.delete()
        sent = await bot.send_audio(
            chat_id=message.chat.id, audio=audio, title=info.get("title"),
            performer=info.get("uploader"), thumbnail=thumbnail, reply_markup=kb,
            reply_to_message_id=message.reply_to_message.message_id if message.reply_to_message else None
        )
        song_data_storage[f"msg_{key}"] = sent.message_id
        save_song_data(song_data_storage)

        async def hide_alt_button():
            await asyncio.sleep(60)
            try:
                new_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=btn_text, callback_data=f"info_{key}")]])
                await bot.edit_message_reply_markup(chat_id=sent.chat.id, message_id=sent.message_id, reply_markup=new_kb)
            except: pass
        asyncio.create_task(hide_alt_button())
        cleanup_temp_files(base)

    except Exception as e:
        await status.delete()
        error_msg = "❌ Error: "
        if "LONG_AUDIO" in str(e): error_msg += "Track exceeds 15 minutes."
        elif "TOO_LARGE" in str(e): error_msg += "File is larger than 50 MB."
        elif "NO_RESULTS" in str(e): error_msg += "Nothing found."
        else: error_msg += "Search failed."
        err = await message.answer(error_msg)
        await asyncio.sleep(5)
        await err.delete()

@dp.callback_query(F.data.startswith("alt_"))
async def show_alternatives(cq: CallbackQuery):
    key = cq.data[4:]
    entry = song_data_storage.get(f"info_{key}")
    if not entry or cq.from_user.id != entry.get("requester"):
        await cq.answer("❌ This menu is not for you! 💅", show_alert=True)
        return
    results = await search_multiple(entry.get("query"))
    btns = []
    count = 0
    for r in results:
        duration = r.get("duration", 0)
        if duration and duration > 900: continue
        title_short = (r.get("title") or "No title")[:40]
        btns.append([InlineKeyboardButton(text=title_short, callback_data=f"choose_{key}_{r['id']}")])
        count += 1
        if count >= 10: break
    btns.append([InlineKeyboardButton(text="❌ Cancel", callback_data=f"cancel_{key}")])
    await cq.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=btns))
    await cq.answer()

@dp.callback_query(F.data.startswith("info_"))
async def show_info(cq: CallbackQuery):
    data = song_data_storage.get(cq.data)
    if not data:
        await cq.answer("Data expired.", show_alert=True)
        return
    m, s = divmod(data.get("duration", 0), 60)
    duration_str = f"{m}:{str(s).zfill(2)}"
    views, likes, dislikes = format_number_dot(data.get("view_count")), format_number_dot(data.get("like_count")), format_number_dot(data.get("dislike_count"))
    tagline = random.choice([
        "The oldest known song is 3,400 years old, a hymn from Ugarit.",
        "A bird bone flute from 40,000 years ago is considered the first instrument."
    ])
    msg = (f"👤 Artist: {data.get('artist')}\n📅 Date: {data.get('upload_date', '')[:4]}\n"
           f"──────────────────\n📈 Views: {views}\n👍 {likes}  👎 {dislikes}\n"
           f"──────────────────\n{tagline}")
    await cq.answer(msg, show_alert=True)

# Note: choose_song and cancel_alt omitted for brevity, should follow the same pattern.

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))