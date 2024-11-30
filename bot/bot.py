import asyncio
import logging
from aiogram import F, Bot, Dispatcher, types
from aiogram.filters.command import Command
import os

from dotenv import load_dotenv
from get_instruction import get_instruction_from_storage
from get_answer import get_answer_from_yandexGPT
from get_text import get_question_from_photo

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

# Обработчики для текстовых сообщений
@dp.message(F.text)
async def handle_text_message(message: types.Message):
    question: str = message.text
    instruction: str = get_instruction_from_storage()
    answer: str = get_answer_from_yandexGPT(instruction, question)
    
    await message.reply(f"{answer}")

# Обработчик для фотографий
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    instruction: str = get_instruction_from_storage()
    question: str = await get_question_from_photo(bot, message)
    answer: str = get_answer_from_yandexGPT(instruction, question)

    await message.reply(f"{answer}")

# Обработчик для других типов сообщений
@dp.message()
async def handle_other(message: types.Message):
    await message.reply("Я могу обработать только текстовое сообщение или фотографию.")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())