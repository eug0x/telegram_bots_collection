import asyncio
import sys
import locale
import importlib.util
import os

def load_strings():
    lang_code = 'en' 

    for var in ['LANG', 'LC_ALL', 'LC_MESSAGES']:
        env_lang = os.environ.get(var)
        if env_lang:
            lang_code = env_lang.split('.')[0].split('_')[0].lower()
            if lang_code and lang_code not in ('c', 'posix'):
                break
    
    if lang_code in ('c', 'posix', 'en'):
        try:
            sys_lang = locale.getdefaultlocale()[0]
            if sys_lang:
                new_lang_code = sys_lang.split('_')[0].lower()
                if new_lang_code:
                    lang_code = new_lang_code
        except Exception:
            pass
            
    base_dir = os.path.dirname(os.path.abspath(__file__))
    lang_file_path = os.path.join(base_dir, 'src', 'language', f'{lang_code}.py')
    
    if not os.path.exists(lang_file_path):
        print(f"⚠️ Language file {lang_code}.py not found. Using English (en).")
        lang_code = 'en'
        lang_file_path = os.path.join(base_dir, 'src', 'language', f'{lang_code}.py')
        
    spec = importlib.util.spec_from_file_location("STR", lang_file_path)
    if spec is None:
        print("❌ Critical error: locale file specification not found.")
        sys.exit(1)
        
    strings_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(strings_module)
    
    return strings_module

STR = load_strings()

from src.client import get_client
from src.actions import delete_history, get_target_entity, get_entity_title


async def get_and_validate_target(client):
    while True:
        try:
            user_input = input(STR.INPUT_ID).strip()
            target_id = int(user_input)
            
            if target_id > 1000000000000 and target_id > 0:
                 target_id = -100 * target_id
            
            print(STR.CHECKING_CHAT)
            entity = await get_target_entity(client, target_id)
            
            if entity:
                title = get_entity_title(entity)
                print(STR.CHAT_CONFIRMED.format(title=title, chat_id=target_id))
                return entity
            else:
                print(STR.CHAT_NOT_FOUND_RETRY.format(chat_id=target_id))
                
        except ValueError:
            print(STR.INVALID_INPUT)
        except Exception as e:
            print(STR.CRITICAL_ERROR.format(error=STR.ERROR_SEARCH.format(error=e)))
            
async def main_menu():
    print(STR.MENU_TITLE)
    print(STR.INIT_CLIENT)
    
    client = await get_client()
    me = await client.get_me()
    
    print(STR.WELCOME.format(name=me.first_name))
    
    target_entity = await get_and_validate_target(client)
    
    while True:
        target_id = target_entity.id
        title = get_entity_title(target_entity)
        
        menu_text = STR.MENU_OPTIONS.format(current_id=f"{title} ({target_id})")
        print(menu_text) 
        
        choice = input(STR.INPUT_CHOICE).strip()

        if choice == '1':
            await delete_history(client, target_entity) 
        elif choice == '2':
            new_entity = await get_and_validate_target(client)
            if new_entity:
                target_entity = new_entity 
                
        elif choice == '3': 
            print(STR.GOODBYE)
            await client.disconnect()
            break
        else:
            print(STR.INVALID_INPUT)

if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        print(STR.STOPPED)
        sys.exit()
    except Exception as e:
        STR = load_strings()
        print(STR.CRITICAL_ERROR.format(error=e))