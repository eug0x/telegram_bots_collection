# History Extractor

I built this tool specifically to recover message history from deleted accounts. When an account is gone, Telegram's built-in search becomes useless since there is no username to click on. Messages just sit there like "dead weight" in the channel.

This script finds them using the permanent **User ID**. Even if the name is just "Deleted Account," the bot will scrape every single message and save it into a clean text file.

### What it does:
* Scrapes every message from a specific user in a channel/group.
* Uses **User ID**, which is the only way to track deleted accounts.
* Saves everything to a `.txt` file with timestamps (good for archives or evidence).

### Setup:
1. Put your credentials in the `.env` file:
   ```env
   API_ID=your_id
   API_HASH=your_hash
   CHANNEL_ID=-100... (target channel ID)
   
2. Install requirements: pip install -r requirements.txt

3. Run: python main.py

Enter the ID, hit the button, and you have the history in a file. Simple as that.
