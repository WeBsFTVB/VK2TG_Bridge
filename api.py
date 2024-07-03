import vk_api
from telegram import Bot

def get_vk_messages(vk_session, user_id, count=5):
    vk = vk_session.get_api()
    messages = vk.messages.getHistory(user_id=user_id, count=count)
    return messages['items']

def send_telegram_message(tg_bot, chat_id, text):
    tg_bot.send_message(chat_id=chat_id, text=text)