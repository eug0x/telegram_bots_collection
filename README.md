# 🚀Telegram Bots Collection🚀

This repository is a collection of various Telegram bots and userbots for any purpose. You are free to use, modify, and integrate them into your own projects. Each bot is located in its own directory with its own setup instructions.

---

## 🤖 Projects List

| Bot Name | Type | Description |
| :--- | :--- | :--- |
| [music_bot](./bots/music_bot) | **Token Bot** | **Music on Demand.** Downloads and sends any song to a group chat in 10-15 seconds via the `music [name]` command. |
| [gui_messenger](./bots/gui_messenger) | **Token Bot** | **Direct GUI Messenger.** A desktop interface to send private messages and media to specific users through your bot. |
| [msg_cleaner](./bots/msg_cleaner) | **Userbot** | **Range Deleter.** Wipes your own messages from any chat/group using text phrases as start and end markers. |
| [music_forwarder](./bots/music_forwarder) | **Userbot** | **Track Migrator.** Transfers songs from external channels to your own, strictly filtering for correct MP3 formats and metadata. |
| [reply_bot](./bots/reply_bot) | **Userbot** | **Target Auto-Responder.** Automatically sends a predefined reply only to a specific user defined in your settings. |
| [user_history_extractor](./bots/user_history_extractor) | **Userbot** | **Full History Scraper.** Downloads all messages from a specific user, including deleted accounts, using only their Telegram ID. |

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


