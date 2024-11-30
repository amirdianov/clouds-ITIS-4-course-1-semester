# Функция для получения инструкции из Yandex Object Storage
import logging
import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()
def get_instruction_from_storage():
    # Создаем сессию для взаимодействия с Yandex Object Storage
    session = boto3.session.Session(
        region_name='ru-central1',
        aws_access_key_id=os.getenv("YANDEX_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("YANDEX_SECRET_KEY"))
    
    s3_client = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    try:
        # Загружаем объект из Yandex Object Storage
        response = s3_client.get_object(Bucket="hw1-vvot25", Key="instruction.txt")
        print(response, '--------')
        instruction = response['Body'].read().decode('utf-8')
        print(instruction, '----------')
        return instruction
    except NoCredentialsError:
        logging.error("Ошибка авторизации в Yandex Object Storage")
        return None
    except Exception as e:
        logging.error(f"Ошибка при получении инструкции из Yandex Object Storage: {str(e)}")
        return None