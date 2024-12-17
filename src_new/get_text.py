import base64
import json
import logging
import os

from dotenv import load_dotenv
import requests

load_dotenv()


def process_image_with_yandex_vision(image_data: str, token: str):
    image_base64 = base64.b64encode(image_data).decode("utf-8")
    data = {"mimeType": "JPEG",
            "languageCodes": ["*"],
            "content": image_base64,
            "model": "page"}

    url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"

    headers= {"Content-Type": "application/json",
            "Authorization": "Bearer {:s}".format(token),
            "x-folder-id": os.getenv("folder_id"),
            "x-data-logging-enabled": "true"}
    

    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            data = response.json()
            # Проверка, есть ли распознанный текст
            if len(data["result"]['textAnnotation']) > 0:
                recognized_text = ""
                for block in data["result"]["textAnnotation"]["blocks"]:
                    for line in block["lines"]:
                        recognized_text += line["text"] + " "
                return recognized_text
            else:
                return None
        else:
            logging.error(f"Ошибка при отправке запроса на OCR: {response.text}")
            return None
    except Exception as e:
        logging.error(f"Ошибка при работе с Yandex OCR API: {e}")
        return None

def get_question_from_photo(message, token):
    try:
        photo_info = message["photo"]
        file_id = photo_info[-1]["file_id"]
        url = f"https://api.telegram.org/bot{os.getenv('tg_bot_key')}/getFile?file_id={file_id}"
        response = requests.get(url)
        if response.status_code == 200:
            file_path = response.json().get('result', {}).get('file_path')
            if file_path:
                file_url = f"https://api.telegram.org/file/bot{os.getenv('tg_bot_key')}/{file_path}"
                image_data = requests.get(file_url).content
                recognized_text = process_image_with_yandex_vision(image_data, token)
                return recognized_text
            else:
                logging.error("Не удалось получить путь к файлу")
                return None
        else:
            return None
    except Exception as e:
        return None
