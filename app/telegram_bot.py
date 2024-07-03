
import logging
import vk_api
from db import session
from models import AuthKeys

def get_vk_token_by_group_id(group_id):
    auth_key = session.query(AuthKeys).filter_by(vk_group_id=str(group_id)).first()
    return auth_key.vk_token if auth_key else None

def handle_telegram_messages(telegram_bot):
    @telegram_bot.message_handler(func=lambda message: True)
    def reply_to_vk(message):
        original_message = message.reply_to_message.text if message.reply_to_message else None
        if original_message:
            # Парсинг оригинального сообщения, чтобы получить ID пользователя ВКонтакте и Group ID
            lines = original_message.split('\n')
            user_id = None
            vk_group_id = None
            for line in lines:
                if line.startswith("ID: "):
                    user_id = line.split(": ")[1]
                if line.startswith("Group ID: "):
                    vk_group_id = line.split(": ")[1]

            if user_id and vk_group_id:
                logging.debug(f"Extracted user_id: {user_id} and vk_group_id: {vk_group_id}")
                vk_token = get_vk_token_by_group_id(vk_group_id)
                logging.debug(f"Auth key for group_id {vk_group_id}: {vk_token}")
                if vk_token:
                    vk_session = vk_api.VkApi(token=vk_token)
                    vk = vk_session.get_api()
                    if vk_group_id.startswith('public'):
                        vk_group_id = vk_group_id.replace('public', '')
                    vk.messages.send(
                        user_id=user_id,
                        message=message.text,
                        random_id=0,
                        from_group=1,
                        group_id=int(vk_group_id)
                    )
                else:
                    logging.warning(f"Не удалось найти токен для группы с ID {vk_group_id}")

    # Запуск поллинга Телеграм-бота
    telegram_bot.polling()
