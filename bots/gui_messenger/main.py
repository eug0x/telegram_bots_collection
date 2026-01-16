import sys
import os
import json
import asyncio
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QListWidgetItem, QLineEdit, QLabel, QFileDialog, QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt, QTimer
from qasync import QEventLoop, asyncSlot
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.types import FSInputFile

# --- Configuration ---
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

CHAT_DIR = "Chats"
os.makedirs(CHAT_DIR, exist_ok=True)
CONTACTS_FILE = "contacts.json"

class TelegramBotRunner:
    def __init__(self):
        self.bot = Bot(token=API_TOKEN)
        self.dp = Dispatcher()
        self.dp.message.register(self.handle_message, F.chat.type == "private")
        self.new_message_callback = None

    async def handle_message(self, message: types.Message):
        contact_id = message.chat.id
        text = message.text or ""
        media_type = "photo" if message.photo else None

        if self.new_message_callback:
            self.new_message_callback({
                "contact_id": contact_id,
                "from_me": False,
                "text": text,
                "media": media_type,
                "message_id": message.message_id,
            })

        self.save_message(contact_id, False, text, media_type, message.message_id)

    def save_message(self, contact_id, from_me, text, media_type, message_id=None):
        path = os.path.join(CHAT_DIR, f"{contact_id}.json")
        history = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                history = json.load(f)
        history.append({
            "from_me": from_me,
            "text": text,
            "media": media_type,
            "message_id": message_id
        })
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

    async def send_message(self, contact_id, text):
        try:
            msg = await self.bot.send_message(contact_id, text)
            self.save_message(contact_id, True, text, None, msg.message_id)
            if self.new_message_callback:
                self.new_message_callback({
                    "contact_id": contact_id,
                    "from_me": True,
                    "text": text,
                    "media": None,
                    "message_id": msg.message_id,
                })
            return True, None
        except Exception as e:
            return False, str(e)

    async def send_photo(self, contact_id, photo_path):
        try:
            photo = FSInputFile(photo_path)
            msg = await self.bot.send_photo(contact_id, photo=photo)
            self.save_message(contact_id, True, f"[Photo: {os.path.basename(photo_path)}]", "photo", msg.message_id)
            if self.new_message_callback:
                self.new_message_callback({
                    "contact_id": contact_id,
                    "from_me": True,
                    "text": f"[Photo: {os.path.basename(photo_path)}]",
                    "media": "photo",
                    "message_id": msg.message_id,
                })
            return True, None
        except Exception as e:
            return False, str(e)

    async def start_polling(self):
        await self.dp.start_polling(self.bot)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TG Desktop Messenger")
        self.resize(800, 600)

        self.contacts_list = QListWidget()
        self.contacts_list.setMaximumWidth(250)

        self.btn_add_contact = QPushButton("Add Contact")
        self.btn_add_contact.clicked.connect(self.add_contact_dialog)

        self.chat_display = QListWidget()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.returnPressed.connect(self.send_text_message)

        self.btn_send_file = QPushButton("Send Photo/GIF")
        self.btn_send_file.clicked.connect(self.send_file)

        self.btn_delete_message = QPushButton("Delete Selected")
        self.btn_delete_message.clicked.connect(self.delete_selected_messages)

        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Contacts:"))
        left_layout.addWidget(self.contacts_list)
        left_layout.addWidget(self.btn_add_contact)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Chat History:"))
        right_layout.addWidget(self.chat_display)
        right_layout.addWidget(self.message_input)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_send_file)
        btn_layout.addWidget(self.btn_delete_message)
        right_layout.addLayout(btn_layout)

        main_layout = QHBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        self.contacts = {}
        self.load_contacts()
        self.contacts_list.currentItemChanged.connect(self.display_chat_history)

        self.bot_runner = TelegramBotRunner()
        self.bot_runner.new_message_callback = self.on_new_message

    def load_contacts(self):
        if os.path.exists(CONTACTS_FILE):
            with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
        else:
            saved = {}

        for filename in os.listdir(CHAT_DIR):
            if filename.endswith(".json"):
                try:
                    contact_id = int(filename.replace(".json", ""))
                    history = self.load_history(contact_id)
                    name = saved.get(str(contact_id), str(contact_id))
                    self.contacts[contact_id] = {"name": name, "history": history}
                    self.contacts_list.addItem(name)
                except: pass

    def save_contacts(self):
        to_save = {str(cid): data["name"] for cid, data in self.contacts.items()}
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(to_save, f, ensure_ascii=False, indent=2)

    def load_history(self, contact_id):
        path = os.path.join(CHAT_DIR, f"{contact_id}.json")
        if not os.path.exists(path): return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_history(self, contact_id):
        path = os.path.join(CHAT_DIR, f"{contact_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.contacts[contact_id]["history"], f, ensure_ascii=False, indent=2)

    def display_chat_history(self, current, previous=None):
        self.chat_display.clear()
        if not current: return

        name = current.text()
        contact_id = next((cid for cid, data in self.contacts.items() if data["name"] == name), None)
        if contact_id is None: return

        for i, msg in enumerate(self.contacts[contact_id]["history"]):
            sender = "Me" if msg["from_me"] else "Them"
            media = f" [{msg['media']}]" if msg["media"] else ""
            item = QListWidgetItem(f"{sender}: {msg['text']}{media}")
            item.setData(Qt.UserRole, i)
            self.chat_display.addItem(item)

    def add_contact_dialog(self):
        contact_text, ok = QInputDialog.getText(self, "Add Contact", "Enter ID:")
        if not (ok and contact_text.strip()): return
        
        contact_text = contact_text.strip()
        name, ok = QInputDialog.getText(self, "Contact Name", "Enter display name:", text=contact_text)
        if not ok: return
        name = name.strip() or contact_text

        if contact_text.startswith("@"):
            asyncio.create_task(self._add_contact_by_username(contact_text, name))
        elif contact_text.isdigit():
            self._add_contact(int(contact_text), name)
        else:
            QMessageBox.warning(self, "Error", "Invalid format")

    async def _add_contact_by_username(self, contact_text, name):
        try:
            chat = await self.bot_runner.bot.get_chat(contact_text[1:])
            QTimer.singleShot(0, lambda: self._add_contact(chat.id, name))
        except Exception as e:
            QTimer.singleShot(0, lambda: QMessageBox.warning(self, "Error", f"Could not find user.\n{e}"))

    def _add_contact(self, contact_id, name):
        if contact_id not in self.contacts:
            self.contacts[contact_id] = {"name": name, "history": []}
            self.contacts_list.addItem(name)
        else:
            self.contacts[contact_id]["name"] = name
        self.save_contacts()
        self.save_history(contact_id)

    @asyncSlot()
    async def send_text_message(self):
        current_item = self.contacts_list.currentItem()
        if not current_item: return

        contact_id = next((cid for cid, d in self.contacts.items() if d["name"] == current_item.text()), None)
        text = self.message_input.text().strip()
        if not text or not contact_id: return
        
        self.message_input.clear()
        success, error = await self.bot_runner.send_message(contact_id, text)
        if not success: QMessageBox.warning(self, "Error", error)

    def send_file(self):
        current_item = self.contacts_list.currentItem()
        if not current_item: return

        path, _ = QFileDialog.getOpenFileName(self, "Select Photo/GIF")
        if not path: return

        contact_id = next((cid for cid, d in self.contacts.items() if d["name"] == current_item.text()), None)
        asyncio.create_task(self._send_file_async(contact_id, path))

    async def _send_file_async(self, contact_id, path):
        success, err = await self.bot_runner.send_photo(contact_id, path)
        if not success: QTimer.singleShot(0, lambda: QMessageBox.warning(self, "Error", err))

    def on_new_message(self, data):
        cid = data["contact_id"]
        if cid not in self.contacts:
            self.contacts[cid] = {"name": str(cid), "history": []}
            self.contacts_list.addItem(str(cid))
            self.save_contacts()

        self.contacts[cid]["history"].append({
            "from_me": data["from_me"], "text": data["text"], 
            "media": data["media"], "message_id": data.get("message_id")
        })
        self.save_history(cid)
        
        current = self.contacts_list.currentItem()
        if current and self.contacts[cid]["name"] == current.text():
            self.display_chat_history(current)

    def delete_selected_messages(self):
        current_item = self.contacts_list.currentItem()
        if not current_item: return
        
        contact_id = next((cid for cid, d in self.contacts.items() if d["name"] == current_item.text()), None)
        selected_items = self.chat_display.selectedItems()
        if not selected_items: return

        indices = sorted([item.data(Qt.UserRole) for item in selected_items], reverse=True)
        for idx in indices:
            msg = self.contacts[contact_id]["history"].pop(idx)
            if msg.get("message_id"):
                asyncio.create_task(self.bot_runner.bot.delete_message(contact_id, msg["message_id"]))

        self.save_history(contact_id)
        self.display_chat_history(current_item)

def main():
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window = MainWindow()
    window.show()
    QTimer.singleShot(0, lambda: asyncio.create_task(window.bot_runner.start_polling()))
    with loop: loop.run_forever()

if __name__ == "__main__":
    main()