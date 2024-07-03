from flask import Flask, request, jsonify
from models import session, ApiKey
from api import get_vk_messages, send_telegram_message
import vk_api
from telegram import Bot

app = Flask(__name__)

@app.route('/store_keys', methods=['POST'])
def store_keys():
    data = request.json
    vk_api_key = data.get('vk_api_key')
    tg_api_key = data.get('tg_api_key')
    if not vk_api_key or not tg_api_key:
        return jsonify({"error": "Missing API keys"}), 400
    
    new_keys = ApiKey(vk_api_key=vk_api_key, tg_api_key=tg_api_key)
    session.add(new_keys)
    session.commit()
    return jsonify({"message": "API keys stored successfully"}), 200

@app.route('/forward_messages', methods=['POST'])
def forward_messages():
    data = request.json
    vk_user_id = data.get('vk_user_id')
    tg_chat_id = data.get('tg_chat_id')
    if not vk_user_id or not tg_chat_id:
        return jsonify({"error": "Missing user or chat ID"}), 400
    
    api_keys = session.query(ApiKey).first()
    vk_session = vk_api.VkApi(token=api_keys.vk_api_key)
    tg_bot = Bot(token=api_keys.tg_api_key)
    
    messages = get_vk_messages(vk_session, vk_user_id)
    
    for message in messages:
        send_telegram_message(tg_bot, tg_chat_id, message['text'])
    
    return jsonify({"message": "Messages forwarded successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
