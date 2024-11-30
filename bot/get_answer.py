import logging
from dotenv import load_dotenv
import requests
import os

load_dotenv()

def get_answer_from_yandexGPT(question: str, instruction: str):
    try:
        url: str = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers: dict = {"Content-Type": "application/json", 
                "Authorization": f"Bearer {os.getenv('IAM_TOKEN')}", 
                "x-folder-id": "b1g35q1e4u30mofm60p4"}

        # Инструкция будет отправлена вместе с вопросом
        data: dict = {
        "modelUri": "gpt://b1g35q1e4u30mofm60p4/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.1,
            "maxTokens": 1000
        },
        "messages": [
            {
            "role": "system",
            "text": instruction,
            },
            {
            "role": "user",
            "text": question,
            }
        ]
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print('ZZZ')
            response_data = response.json()
            return response_data['result']['alternatives'][0]['message']["text"]  # предполагаем, что ответ возвращается в поле 'text'
        else:
            logging.error(f"Error: {response.status_code} {response.text}")
            return "Не удалось получить ответ от YandexGPT."
    except Exception as e:
        logging.error(f"Exception occurred: {str(e)}")