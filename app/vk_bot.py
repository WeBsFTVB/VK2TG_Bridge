import vk_api
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from db import session
from models import AuthKeys

def forward_message_to_telegram(vk_session, vk_group_id, vk_token, telegram_bot, telegram_chat_id):
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            user_info = vk.users.get(user_ids=user_id)[0]
            full_name = f"{user_info['first_name']} {user_info['last_name']}"
            message_text = event.text
            date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(event.timestamp))

            telegram_bot.send_message(chat_id=telegram_chat_id, 
                                      text=f"Дата: {date}\nИмя: {full_name}\nID: {user_id}\nСообщение: {message_text}\nGroup ID: {vk_group_id}")

def get_vk_token_by_group_id(group_id):
    auth_key = session.query(AuthKeys).filter_by(vk_group_id=str(group_id)).first()
    return auth_key.vk_token if auth_key else None
