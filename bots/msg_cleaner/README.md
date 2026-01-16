# Telegram Messages Cleaner

command-line utility built with `Telethon` to safely and precisely delete your own outgoing messages within a specific range defined by text checkpoints in any Telegram chat, group, or channel.

---

## ✨ Features

* **Precise Range Deletion:** Define the start and end of the deletion range using specific text phrases (checkpoints).

* **Safety Measures:** Implements random, short delays between message deletions and longer pauses every 100 messages to prevent account suspension due to Telegram's rate limits.

* **Automatic Localization:** Automatically detects your operating system's language settings and loads the corresponding interface text.

## 🌐 Supported Languages

Currently supported languages:

* **English** (`en.py`) 
* **Chinese** (`zh.py`)
* **Spanish** (`es.py`)

To add a new language, simply create a file named `**.py` inside the `src/language/` directory and translate all string constants.

## 📁 Structure

 ```bash
├── .env
├── main.py
└── src/
    ├── config.py
    ├── client.py
    ├── language/
    └── actions.py
```
## 🚀 Usage

1.  **Run the script:**

    ```bash
    python main.py
    ```

2.  **Login:** The first time you run the script, `Telethon` will prompt you to enter your phone number, password, and the code sent by Telegram. This creates the session file (`my_session_name.session`).

3.  **Enter Target ID:** Input the numerical ID of the user, group, or channel you wish to clean.
    * **User/Group ID:** Standard numerical ID (e.g., `123456789`).
    * **Public Channel ID:** Use the large positive ID (e.g., `1646810103`), and the script will automatically convert it to the required negative format.

4. **Show Chat/User ID:**  
   Go to Telegram’s **Advanced Settings**, scroll to the bottom, open **Experimental Settings**, and enable **“Show IDs”**.  
   After that, Telegram will display the ID of any chat, group, or user directly in its info panel.

### Menu Options

| Option | Action |
| :---: | :--- |
| **1** | **Delete messages in range:** Starts the history cleaning process between two checkpoints. |
| **2** | **Change interlocutor ID:** Allows you to switch to a different chat or user. |
| **3** | **Exit:** Disconnects the client and closes the program. |

### Setting Checkpoints (Option 1)

When you choose **Option 1**, the bot will ask for two key phrases:

1.  **Start Checkpoint (Newest Message):** Enter a unique phrase from the **newest message** you want to delete.
2.  **End Checkpoint (Oldest Message):** Enter a unique phrase from the **oldest message** you want to delete.

> **❗ CRITICAL NOTE:** **Do not** use phrases that repeat frequently (like "hello" or "ok") for the **End Checkpoint**. Always choose a **unique, long, or specific phrase** to ensure the entire desired range is selected for deletion.


## 🛠️ Installation & Setup

### Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/eug0x/telegram_msg_cleaner
    
    cd tg_manager
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment (`.env` file):**
    Create a file named **`.env`** in the root directory (`tg_manager/`) and populate it with your Telegram credentials:
    * A Telegram API Key (`API_ID` and `API_HASH`). You can get one from [my.telegram.org](https://my.telegram.org).

    ```env
    python main.py
    ```

## 🌟 Future Updates

### 1. Precision & Logging Upgrade
* **Message Link/ID Input:** Checkpoints will transition from text phrases to **direct message links or IDs** for guaranteed accuracy and better logging.

### 2. Performance & Scalability
* **Dynamic Scan Range:** Users will be able to set a **custom limit** for the message scan (e.g., scan the last 500 or 50,000 messages) to significantly speed up searches or find very old history.

### 3. Expanded Deletion & Analytics
* **Delete Others' Messages:** Add the option to delete messages sent by other users (requires admin privileges).
* **Time-Based Message Count:** Introduce a feature to scan and **calculate the total number of messages** sent within a **private chat** over a specified date range.
---

