# Reply Bot

A Telegram Userbot that waits for a specific user to message you, then replies with the latest post from a specified channel after a delay.

## Features
* **Smart Delay:** Waits for a set amount of seconds before responding.
* **Anti-Flood:** Updates the reply target if multiple messages are sent during the delay.

## Setup
1. Create a `.env` file in this directory:
   ```env
   API_ID=your_id
   API_HASH=your_hash
   TARGET_USER_ID=user_id_to_respond_to
   AUTO_REPLY_TEXT="Hi, this is an auto-responder..."