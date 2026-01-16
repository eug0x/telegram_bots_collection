# 🚀Telegram Bots Collection🚀

This repository is a collection of various Telegram bots and userbots for any purpose. You are free to use, modify, and integrate them into your own projects. Each bot is located in its own directory with its own setup instructions.

---

## 🤖 Projects List

| Bot Name | Type | Description |
| :--- | :--- | :--- |
| [music_bot](./bots/music_bot) | **Token Bot** | **Efficient Music Downloader.** Uses `yt-dlp` with a smart renaming trick to skip FFmpeg conversion. Features an interactive UI to pick alternative tracks if the first search result is wrong. |
| [gui_messenger](./bots/gui_messenger) | **Token Bot** | **Desktop Admin Panel.** A PySide6 GUI that allows you to manage bot-to-user conversations, send mass alerts, and share photos directly from your PC without touching code. |
| [msg_cleaner](./bots/msg_cleaner) | **Userbot** | **Precision History Purge.** Deletes your messages in any chat based on text "checkpoints" (start/end phrases). Includes built-in safety delays to avoid Telegram rate limits. |
| [music_forwarder](./bots/music_forwarder) | **Userbot** | **DB Populator.** Transfers music between channels with **Fuzzy Matching** (skips duplicates even with different titles) and strict MP3 quality filters. Feeds your music bot's database. |
| [reply_bot](./bots/reply_bot) | **Userbot** | **Instant Auto-Responder.** A personal assistant that monitors chats and replies to specific users with pre-defined messages instantly using the Telethon MTProto engine. |
| [user_history_extractor](./bots/user_history-extractor) | **Userbot** | **Forensic History Tool.** Scrapes and recovers message history and media from deleted accounts or hidden profiles using their unique Telegram User ID. |

---


> * **Token Bot:** Requires a `BOT_TOKEN`. Create one via [@BotFather](https://t.me/BotFather) on Telegram.
> * **Userbot:** Requires `API_ID` and `API_HASH`. You can get these by creating an "App" on the official [my.telegram.org](https://my.telegram.org) portal.

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Libraries:** Telethon, Aiogram 3.x, PySide6, qasync..
* **Config:** All sensitive data is stored in `.env` files.

---

## 📜 Disclaimer & License

The author of these bots and modules assumes **no responsibility** for how these tools are used or for any actions taken by the bots. By using this code, you agree that you are solely responsible for compliance with Telegram's Terms of Service and any potential consequences (such as account restrictions). Use them at your own risk.

[MIT LICENSE](./LICENSE) 

---
