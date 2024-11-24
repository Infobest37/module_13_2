from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Исправлено
import asyncio

api = "7945740698:AAEInDjzg83i0KA-71qopdj-KFwhISwCNvI"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())  # Исправлено
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот помогающий твоему здоровью.")
@dp.message_handler()
async def send_welcome(message):
        print("Вам пришло сообщение")
        await message.reply("Введите команду /start, чтобы начать общение.'")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
