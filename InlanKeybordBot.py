from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Исправлено
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio


api = "7945740698:AAEInDjzg83i0KA-71qopdj-KFwhISwCNvI"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard делает кнопки компактными
button = KeyboardButton(text="Рассчитать")
button_2 = KeyboardButton(text="Информация")
kb.add(button, button_2)

ikb = InlineKeyboardMarkup(row_width=1)
button = InlineKeyboardButton(text='Рассчитать норму калорий' , callback_data='calories')
button_2 = InlineKeyboardButton(text='Формулы расчёта' , callback_data='formulas')

ikb.add(button)
ikb.add(button_2)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Рады вас видеть", reply_markup=start_menu)

@dp.callback_query_handler(text="button")
async def button(call: types.CallbackQuery):
    await call.message.answer("Информация о боте")
    await call.answer()

start_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="shop"),
               KeyboardButton(text='donate')]], resize_keyboard=True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)