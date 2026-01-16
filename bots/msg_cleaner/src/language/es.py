MENU_TITLE = "\n--- Telegram Msg Cleaner ---"
INIT_CLIENT = "Inicializando cliente..."
WELCOME = "👋 ¡Hola, {name}!"

INPUT_ID = "Introduce el ID (usuario o canal): "
CHECKING_CHAT = "🔍 Comprobando chat..."
CHAT_CONFIRMED = "✅ Chat encontrado con éxito: {title} (ID: {chat_id})."
CHAT_NOT_FOUND_RETRY = "❌ No se encontró el chat con ID {chat_id}. Inténtalo de nuevo."
INPUT_NEW_ID = "Introduce el NUEVO ID del interlocutor: "

MENU_OPTIONS = """
📋 MENÚ:
1. Eliminar mensajes en el rango (Start Checkpoint → End Checkpoint)
2. Cambiar ID del interlocutor (Actual: {current_id})
3. Salir
"""
INPUT_CHOICE = "\n(1-3): "
GOODBYE = "👋"
INVALID_INPUT = "❌ Entrada no válida, intenta de nuevo."
STOPPED = "\n🛑 Programa detenido."
CRITICAL_ERROR = "\n❌ Ocurrió un error crítico: {error}"
ERROR_SEARCH = "Error al buscar: {error}" 

INPUT_START_PHRASE = "\n 1 Introduce la frase del mensaje MÁS RECIENTE: "
INPUT_END_PHRASE = " 2 Introduce la frase del mensaje MÁS ANTIGUO: "
WARN_EMPTY = "⚠️ Entrada vacía."
MSG_LIMIT_SCAN = "⏳ Escaneando tus últimos {limit} mensajes..."

MSG_FOUND = "✅ Mensaje encontrado: \"{text}...\" (ID: {msg_id})"

START_MSG_NOT_FOUND = "❌ Mensaje Start Checkpoint (nuevo) con texto '{text}' no encontrado en los últimos {limit}."
END_MSG_NOT_FOUND = "❌ Mensaje End Checkpoint (antiguo) con texto '{text}' no encontrado en los últimos {limit}."
RANGE_ERROR = "⚠️ Error de rango: Start ID ({start_id}) debe ser MÁS RECIENTE que End ID ({end_id}). Verifica el orden de las frases."
ZERO_TO_DELETE = "🤷‍♂️ Rango establecido, pero no hay mensajes salientes para eliminar."

CONFIRM_DELETE = "🗑️ Se encontraron {count} mensajes para eliminar.\nInicio (Nuevo) ID: {start_id}\nFin (Antiguo) ID: {end_id}\n❗ ¿Estás seguro? 'sí' o cualquier mensaje para cancelar: "
CANCELLED = "🚫 Cancelado."
CONFIRM_YES = "sí"
START_DELETING = "\n🚀 Comenzando eliminación..."
DELETED_LOG = "[{current}/{total}] Eliminado ID: {msg_id}"
PAUSE_LONG = "☕ Pausa de 5 segundos por seguridad..."
DELETE_ERROR = "⚠️ Error con ID {msg_id}: {error}"
DONE = "\n🏁 Limpieza completada!"
