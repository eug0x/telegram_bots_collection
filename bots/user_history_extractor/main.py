import sys
import os
import asyncio
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit, QMessageBox
)
from PySide6.QtCore import QThread, Signal
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()
try:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
except (TypeError, ValueError):
    print("Error: Check API_ID, API_HASH and CHANNEL_ID in .env file")
    sys.exit(1)

# Universal session name for easy migration
SESSION_NAME = 'shared_account'

class SearchWorker(QThread):
    log = Signal(str)
    done = Signal(int, str)
    error = Signal(str)

    def __init__(self, user_input: str):
        super().__init__()
        self.user_input = user_input.strip()

    def run(self):
        # Create event loop for Telethon in QThread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
        found_messages = []

        try:
            with client:
                # Get user entity by ID or Username
                if self.user_input.isdigit():
                    user = client.get_entity(int(self.user_input))
                else:
                    user = client.get_entity(self.user_input.lstrip('@'))

                peer = InputPeerUser(user.id, user.access_hash)
                self.log.emit(f"📥 Found user: {user.first_name or 'No Name'} (ID: {user.id})")
                self.log.emit(f"🔎 Searching messages in channel: {CHANNEL_ID}...")

                count = 0
                # Fetching messages
                for message in client.iter_messages(CHANNEL_ID, from_user=peer, reverse=True):
                    text = message.text or "<media/empty>"
                    time_str = message.date.strftime("[%Y-%m-%d %H:%M:%S]") if message.date else "[unknown]"
                    found_messages.append(f"{time_str} {text}")
                    count += 1
                    if count % 20 == 0:
                        self.log.emit(f"⏳ Progress: {count} messages found...")

        except Exception as e:
            self.error.emit(f"Connection Error: {e}")
            return

        if not found_messages:
            self.done.emit(0, "")
            return

        # Save to file
        filename = f"history_user_{user.id}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Chat History for User ID: {user.id}\n{'='*30}\n\n")
            for msg in reversed(found_messages):
                f.write(msg.strip() + "\n\n")

        self.done.emit(len(found_messages), filename)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TG History Extractor")
        self.resize(500, 400)

        layout = QVBoxLayout(self)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Enter User ID or @username")
        layout.addWidget(self.input)

        self.button = QPushButton("Extract History")
        layout.addWidget(self.button)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        layout.addWidget(self.log_display)

        self.button.clicked.connect(self.start_search)

    def start_search(self):
        user_input = self.input.text().strip()
        if not user_input:
            QMessageBox.warning(self, "Error", "Please enter a User ID or Username")
            return

        self.log_display.clear()
        self.log_display.append("🚀 Initializing...")
        self.button.setEnabled(False)

        self.worker = SearchWorker(user_input)
        self.worker.log.connect(self.log_display.append)
        self.worker.error.connect(self.on_error)
        self.worker.done.connect(self.on_done)
        self.worker.start()

    def on_error(self, message):
        self.log_display.append(f"❌ {message}")
        self.button.setEnabled(True)

    def on_done(self, count, filename):
        if count == 0:
            self.log_display.append("⚠ No messages found for this user in this channel.")
        else:
            self.log_display.append(f"✅ Success! Found {count} messages.")
            self.log_display.append(f"📁 Saved to: {filename}")
        self.button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())