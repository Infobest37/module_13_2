from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Исправлено
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())  # Исправлено

class UserState(StatesGroup):

    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот помогающий твоему здоровью")


@dp.message_handler(text=["Calories"])
async def set_age(message: types.Message):
    await message.answer(" Ведите свой возраст")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state: FSMContext):
    await state.update_data(age=int(message.text))
    age_data = await state.get_data()
    await message.answer(f"Твой возраст {age_data['age']} ")
    await message.answer(f"Введите свой рост")
    await UserState.growth.set()
    return age_data
#
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state: FSMContext):
     await state.update_data(growth=int(message.text))
     growth_data = await state.get_data()
     await message.answer(f"Твой рост {growth_data['growth']} ")
     await message.answer(f"Введите свой вес")
     await UserState.weight.set()
     return growth_data
@dp.message_handler(state=UserState.weight)
async def set_calories(message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    data = await state.get_data()
    age = data["age"]
    growth = data["growth"]
    weight = data["weight"]
    calories = 10 * weight + 6.25 * growth - 5 * age + 5  # Формула для мужчин (можно настроить)

    await message.answer(
        f"Ваши данные:\nВозраст: {age}\nРост: {growth} см\nВес: {weight} кг.\n"
        f"Ваша норма калорий: {calories:.2f} ккал. в сутки"
    )
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
