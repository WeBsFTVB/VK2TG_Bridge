import sys
import threading
import telebot
import vk_api
from db import init_db, session
from models import AuthKeys
from vk_bot import forward_message_to_telegram, get_vk_token_by_group_id
from telegram_bot import handle_telegram_messages

def get_auth_keys():
    return session.query(AuthKeys).all()

def add_auth_key(vk_group_id, vk_token, telegram_bot_token, telegram_chat_id):
    new_auth_key = AuthKeys(
        vk_group_id=vk_group_id,
        vk_token=vk_token,
        telegram_bot_token=telegram_bot_token,
        telegram_chat_id=telegram_chat_id
    )
    session.add(new_auth_key)
    session.commit()

if __name__ == "__main__":
    init_db()
    
    if len(sys.argv) == 5:
        vk_group_id = sys.argv[1]
        vk_token = sys.argv[2]
        telegram_bot_token = sys.argv[3]
        telegram_chat_id = sys.argv[4]

        add_auth_key(vk_group_id, vk_token, telegram_bot_token, telegram_chat_id)
        print("Ключи авторизации успешно добавлены в базу данных.")
    else:
        auth_keys_list = get_auth_keys()

        for auth_keys in auth_keys_list:
            vk_session = vk_api.VkApi(token=auth_keys.vk_token)
            telegram_bot = telebot.TeleBot(auth_keys.telegram_bot_token)

            threading.Thread(target=forward_message_to_telegram, args=(vk_session, auth_keys.vk_group_id, auth_keys.vk_token, telegram_bot, auth_keys.telegram_chat_id)).start()
            threading.Thread(target=handle_telegram_messages, args=(telegram_bot,)).start()
