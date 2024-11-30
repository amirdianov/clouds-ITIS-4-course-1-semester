import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import os

from dotenv import load_dotenv

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Подгружаем переменные окружения
load_dotenv()

# Объект бота
bot = Bot(token=os.getenv("TG_BOT_KEY"))

# Диспетчер
dp = Dispatcher()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Я помогу подготовить ответ на экзаменационный вопрос по дисциплине 'Операционные системы'. \nПришлите мне фотографию с вопросом или наберите его текстом.")

# Хэндлер на команду /help
@dp.message(Command("help"))
async def cmd_start(message: types.Message):
    await message.answer("Я помогу подготовить ответ на экзаменационный вопрос по дисциплине 'Операционные системы'. \nПришлите мне фотографию с вопросом или наберите его текстом.")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())