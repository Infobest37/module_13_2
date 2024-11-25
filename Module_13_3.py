
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Исправлено
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())  # Исправлено
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Я рад что ты с нами!")
@dp.message_handler(text = ["Привет", "привет"])
async def send_welcome(message):
        print("Вам пришло сообщение")
        await message.reply("Введите команду /start, чтобы начать общение.'")

@dp.message_handler(text = ["Хочу найти глобус"])
async def send_welcome(message):
        print("Вам пришло сообщение")
        await message.reply("Я помогу тебе, дай мне минуту")


@dp.message_handler()
async def echo(message):
    print("У нас новое сообщение")
    await message.answer(message.text.upper())
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
