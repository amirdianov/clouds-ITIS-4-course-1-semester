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
        aws_access_key_id=os.getenv("yandex_access_key"),
        aws_secret_access_key=os.getenv("yandex_secret_key"))
    
    s3_client = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net'
    )
    try:
        # Загружаем объект из Yandex Object Storage
        response = s3_client.get_object(Bucket="vvot-25-hw1-bucket", Key="instruction.txt")
        instruction = response['Body'].read().decode('utf-8')
        return instruction
    except NoCredentialsError:
        return None
    except Exception as e:
        return None