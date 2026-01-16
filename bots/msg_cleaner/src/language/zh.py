MENU_TITLE = "\n--- Telegram Msg Cleaner ---"
INIT_CLIENT = "正在初始化客户端..."
WELCOME = "👋 你好, {name}!"

INPUT_ID = "输入ID（用户或频道）："
CHECKING_CHAT = "🔍 正在检查聊天..."
CHAT_CONFIRMED = "✅ 聊天成功找到: {title} (ID: {chat_id})。"
CHAT_NOT_FOUND_RETRY = "❌ 未找到ID为 {chat_id} 的聊天。请重试。"
INPUT_NEW_ID = "输入新的聊天对象ID："

MENU_OPTIONS = """
📋 菜单:
1. 删除范围内的消息 (Start Checkpoint → End Checkpoint)
2. 更改聊天对象ID (当前: {current_id})
3. 退出
"""
INPUT_CHOICE = "\n(1-3): "
GOODBYE = "👋"
INVALID_INPUT = "❌ 输入无效，请重试。"
STOPPED = "\n🛑 程序已停止。"
CRITICAL_ERROR = "\n❌ 发生严重错误: {error}"
ERROR_SEARCH = "搜索错误: {error}" 

INPUT_START_PHRASE = "\n 1 输入最新消息中的短语："
INPUT_END_PHRASE = " 2 输入最旧消息中的短语："
WARN_EMPTY = "⚠️ 输入为空。"
MSG_LIMIT_SCAN = "⏳ 正在扫描您最近的 {limit} 条消息..."

MSG_FOUND = "✅ 找到消息: \"{text}...\" (ID: {msg_id})"

START_MSG_NOT_FOUND = "❌ 未在最近 {limit} 条消息中找到 Start Checkpoint 消息（新）: '{text}'。"
END_MSG_NOT_FOUND = "❌ 未在最近 {limit} 条消息中找到 End Checkpoint 消息（旧）: '{text}'。"
RANGE_ERROR = "⚠️ 范围错误: Start ID ({start_id}) 必须比 End ID ({end_id}) 新。请检查短语顺序。"
ZERO_TO_DELETE = "🤷‍♂️ 已设置范围，但没有可删除的外发消息。"

CONFIRM_DELETE = "🗑️ 找到 {count} 条消息可删除。\n起始 (新) ID: {start_id}\n结束 (旧) ID: {end_id}\n❗ 确定吗？输入 '是' 或任何消息取消: "
CANCELLED = "🚫 已取消。"
CONFIRM_YES = "是"
START_DELETING = "\n🚀 开始删除..."
DELETED_LOG = "[{current}/{total}] 已删除 ID: {msg_id}"
PAUSE_LONG = "☕ 为安全暂停5秒..."
DELETE_ERROR = "⚠️ ID {msg_id} 出错: {error}"
DONE = "\n🏁 清理完成！"
