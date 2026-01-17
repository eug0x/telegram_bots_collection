# Secret Message

Hey! This is a simple yet powerful Telegram bot that lets you send self-destructing secret messages in any chat. The coolest part? It wrks via **Inline Mode**, so you don't even have to add the bot to a group to use it

## How it works
1. **In any chat**, type `@YourBotUsername @recipient_username Your secret message`.
2. A pop-up will appear - click it to send.
3. The recipient gets a notification with a "View Secret Message" button.
4. Once they click it, the message is shown as an alert, and the **button vanishes forever**.

## Features
- **No Database:** Messages are stored in RAM. If the bot restarts, all secrets vanish. Maximum privacy.
- **Self-Destruct:** One click, one view. That's it.
- **Anti-Peeking:** If anyone other than the intended recipient clicks the button, they get a "This secret is not for you" alert.
- **Smart Cache:** Automatically clears old unread messages to keep the server light.

## Setup
1. Create a `.env` file based on `env.txt`.
2. Install requirements: `pip install -r requirements.txt`
3. Run: `python main.py`