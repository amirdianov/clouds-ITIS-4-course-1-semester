import requests
import os
import json
from get_instruction import get_instruction_from_storage
from get_answer import get_answer_from_yandexGPT
from get_text import get_question_from_photo

TG_BOT_TOKEN = os.getenv("tg_bot_key")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TG_BOT_TOKEN}"

# Функция для отправки сообщений через Telegram Bot API
def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, data=payload)
    return response


# Хэндлер для команды /start
def handle_start(message):
    chat_id = message["chat"]["id"]
    send_message(chat_id, "Я помогу подготовить ответ на экзаменационный вопрос по дисциплине 'Операционные системы'. \nПришлите мне фотографию с вопросом или наберите его текстом.")

# Хэндлер для команды /help
def handle_help(message):
    chat_id = message["chat"]["id"]
    send_message(chat_id, "Я помогу подготовить ответ на экзаменационный вопрос по дисциплине 'Операционные системы'. \nПришлите мне фотографию с вопросом или наберите его текстом.")

# Обработчик текстовых сообщений
def handle_text_message(message, access_token):
    chat_id = message["chat"]["id"]
    question = message["text"]
    instruction = get_instruction_from_storage()
    answer = get_answer_from_yandexGPT(instruction, question, access_token)
    send_message(chat_id, f"{answer}")

# Обработчик фотографий
def handle_photo(message, access_token):
    chat_id = message["chat"]["id"]
    instruction = get_instruction_from_storage()
    question = get_question_from_photo(message, access_token)
    answer = get_answer_from_yandexGPT(instruction, question, access_token)
    send_message(chat_id, f"{answer}")

# Обработчик других типов сообщений
def handle_other(message):
    chat_id = message["chat"]["id"]
    send_message(chat_id, "Я могу обработать только текстовое сообщение или фотографию.")

# Основной хэндлер для обработки вебхуков
def handler(event, context):
    # Извлекаем JSON тело запроса
    json_str = json.loads(event['body'])
    access_token = context.token['access_token']
    # Проверяем, что в запросе есть объект обновления
    if "message" not in json_str:
        return json.dumps({"status": "error", "message": "Invalid request"}), 400

    message = json_str["message"]
    try:
        if "text" in message:
            text = message["text"]
            if text == "/start":
                handle_start(message)
            elif text == "/help":
                handle_help(message)
            else:
                handle_text_message(message, access_token=access_token)
        elif "photo" in message:
            handle_photo(message, access_token=access_token)
        else:
            handle_other(message)
        return {
            'statusCode': 200
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'error': e
        }
