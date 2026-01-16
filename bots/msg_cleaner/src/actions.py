import asyncio
import random
from telethon import TelegramClient
import sys

def get_entity_title(entity):
    if hasattr(entity, 'first_name') and entity.first_name:
        return entity.first_name
    elif hasattr(entity, 'title') and entity.title:
        return entity.title
    return str(entity.id)

async def get_target_entity(client: TelegramClient, target_id: int):
    try:
        entity = await client.get_entity(target_id)
        return entity
    except Exception:
        async for dialog in client.iter_dialogs():
            if dialog.entity.id == target_id:
                return dialog.entity
    return None

async def delete_history(client: TelegramClient, entity):
    
    stop_text_newest = input(STR.INPUT_START_PHRASE).strip().lower()
    stop_text_oldest = input(STR.INPUT_END_PHRASE).strip().lower()

    if not stop_text_newest or not stop_text_oldest:
        print(STR.WARN_EMPTY)
        return
    
    limit_check = 20000
    print(STR.MSG_LIMIT_SCAN.format(limit=limit_check))
    
    all_messages = await client.get_messages(entity, limit=limit_check)
    my_messages = [msg for msg in all_messages if msg and msg.out]
    
    start_msg = None
    end_msg = None   
    
    for msg in my_messages:
        if msg.message and stop_text_newest in msg.message.lower():
            if start_msg is None or msg.id > start_msg.id:
                start_msg = msg
    
    for msg in my_messages:
        if msg.message and stop_text_oldest in msg.message.lower():
            if end_msg is None or msg.id > end_msg.id:
                end_msg = msg
    
    if not start_msg:
        print(STR.START_MSG_NOT_FOUND.format(text=stop_text_newest, limit=limit_check))
        return
    
    if not end_msg:
        print(STR.END_MSG_NOT_FOUND.format(text=stop_text_oldest, limit=limit_check))
        return

    if start_msg.id < end_msg.id:
        print(STR.RANGE_ERROR.format(start_id=start_msg.id, end_id=end_msg.id))
        return
        
    print(STR.MSG_FOUND.format(text=start_msg.message[:30], msg_id=start_msg.id) + " (Start Checkpoint)")
    print(STR.MSG_FOUND.format(text=end_msg.message[:30], msg_id=end_msg.id) + " (End Checkpoint)")

    to_delete = [
        msg for msg in my_messages 
        if end_msg.id <= msg.id <= start_msg.id
    ]
    
    count = len(to_delete)

    if count == 0:
        print(STR.ZERO_TO_DELETE)
        return

    confirm = input(STR.CONFIRM_DELETE.format(
        count=count, 
        start_id=start_msg.id, 
        end_id=end_msg.id
    )).strip().lower()

    if confirm != STR.CONFIRM_YES:
        print(STR.CANCELLED)
        return

    print(STR.START_DELETING)
    for index, msg in enumerate(to_delete, start=1):
        try:
            await client.delete_messages(entity, msg.id)
            print(STR.DELETED_LOG.format(current=index, total=count, msg_id=msg.id))
            
            await asyncio.sleep(random.uniform(0.3, 0.7))
            
            if index % 100 == 0:
                print(STR.PAUSE_LONG)
                await asyncio.sleep(5)
                
        except Exception as e:
            print(STR.DELETE_ERROR.format(msg_id=msg.id, error=e))

    print(STR.DONE)