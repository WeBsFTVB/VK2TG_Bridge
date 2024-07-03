# VK to Telegram Forwarder

Этот проект пересылает сообщения из ВКонтакте в Телеграм и наоборот.

## Установка

1. Клонируйте репозиторий.
2. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

3. Настройте базу данных в `app/config.py`.

## Использование

### Добавление ключей авторизации

```sh
python app/main.py <vk_group_id> <vk_token> <telegram_bot_token> <telegram_chat_id>
