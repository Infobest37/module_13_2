from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Исправлено
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())  # Исправлено

# Создаем клавиатуру
kb = ReplyKeyboardMarkup(resize_keyboard=True)  # resize_keyboard делает кнопки компактными
button = KeyboardButton(text="Рассчитать")
button_2 = KeyboardButton(text="Информация")
kb.add(button, button_2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, помогающий следить за здоровьем. Выберите действие:", reply_markup=kb)

@dp.message_handler(text="Рассчитать")
async def set_age(message: types.Message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("Введите свой рост (в см):")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=int(message.text))
    await message.answer("Введите свой вес (в кг):")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data["age"]
    growth = data["growth"]
    weight = data["weight"]
    calories = 10 * weight + 6.25 * growth - 5 * age + 5  # Формула для мужчин (можно настроить)

    await message.answer(
        f"Ваши данные:\nВозраст: {age}\nРост: {growth} см\nВес: {weight} кг.\n"
        f"Ваша норма калорий: {calories:.2f} ккал. в сутки",
        reply_markup=kb  # Возвращаем клавиатуру
    )
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
