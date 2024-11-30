import base64
import json
import logging
import os

from dotenv import load_dotenv
import requests

load_dotenv()


async def process_image_with_yandex_vision(image_url: str):
    data = {"mimeType": "JPEG",
            "languageCodes": ["*"],
            "content": base64.b64encode(image_url.getvalue()).decode("utf-8"),
            "model": "page"}

    url = "https://ocr.api.cloud.yandex.net/ocr/v1/recognizeText"

    headers= {"Content-Type": "application/json",
            "Authorization": "Bearer {:s}".format(os.getenv("IAM_TOKEN")),
            "x-folder-id": os.getenv("FOLDER_ID"),
            "x-data-logging-enabled": "true"}
    

    try:
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        print(response.text)
        if response.status_code == 200:
            data = response.json()
            print(data["result"])
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

async def get_question_from_photo(bot, message):
    file_id = message.photo[-1].file_id  # берем самое большое фото
    file = await bot.get_file(file_id)
    
    # Получаем путь к файлу
    file_path = file.file_path
    
    # Скачиваем фото как бинарные данные
    photo_data = await bot.download_file(file_path)
    
    # Отправляем фото на Яндекс Vision API (как base64)

    recognized_text = await process_image_with_yandex_vision(photo_data)
    return recognized_text