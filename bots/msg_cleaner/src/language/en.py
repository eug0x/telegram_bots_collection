MENU_TITLE = "\n--- Telegram Msg Cleaner ---"
INIT_CLIENT = "Initializing client..."
WELCOME = "👋 Hello, {name}!"

INPUT_ID = "Enter ID (user or channel): "
CHECKING_CHAT = "🔍 Checking chat..."
CHAT_CONFIRMED = "✅ Chat successfully found: {title} (ID: {chat_id})."
CHAT_NOT_FOUND_RETRY = "❌ Chat with ID {chat_id} not found. Try again."
INPUT_NEW_ID = "Enter NEW chat partner ID: "

MENU_OPTIONS = """
📋 MENU:
1. Delete messages in range (Start Checkpoint → End Checkpoint)
2. Change chat partner ID (Current: {current_id})
3. Exit
"""
INPUT_CHOICE = "\n(1-3): "
GOODBYE = "👋"
INVALID_INPUT = "❌ Invalid input, try again."
STOPPED = "\n🛑 Program stopped."
CRITICAL_ERROR = "\n❌ Critical error occurred: {error}"
ERROR_SEARCH = "Error searching: {error}" 

INPUT_START_PHRASE = "\n 1 Enter phrase from the NEWEST message: "
INPUT_END_PHRASE = " 2 Enter phrase from the OLDEST message: "
WARN_EMPTY = "⚠️ Empty input."
MSG_LIMIT_SCAN = "⏳ Scanning your last {limit} messages..."

MSG_FOUND = "✅ Message found: \"{text}...\" (ID: {msg_id})"

START_MSG_NOT_FOUND = "❌ Start Checkpoint message (new) with text '{text}' not found in last {limit}."
END_MSG_NOT_FOUND = "❌ End Checkpoint message (old) with text '{text}' not found in last {limit}."
RANGE_ERROR = "⚠️ Range error: Start ID ({start_id}) must be NEWER than End ID ({end_id}). Check that you entered phrases in correct order."
ZERO_TO_DELETE = "🤷‍♂️ Range set, but there are no outgoing messages to delete."

CONFIRM_DELETE = "🗑️ Found {count} messages to delete.\nStart (New) ID: {start_id}\nEnd (Old) ID: {end_id}\n❗ Are you sure? 'yes' or any message to cancel: "
CANCELLED = "🚫 Cancelled."
CONFIRM_YES = "yes"
START_DELETING = "\n🚀 Starting deletion..."
DELETED_LOG = "[{current}/{total}] Deleted ID: {msg_id}"
PAUSE_LONG = "☕ 5-second pause for safety..."
DELETE_ERROR = "⚠️ Error with ID {msg_id}: {error}"
DONE = "\n🏁 Cleanup complete!"
