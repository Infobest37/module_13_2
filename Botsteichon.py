from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Исправлено
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio


api = "7945740698:AAEInDjzg83i0KA-71qopdj-KFwhISwCNvI"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())  # Исправлено

class UserState(StatesGroup):
    adress = State()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await UserState.adress.set()

@dp.message_handler(text=["Заказать"])
async def buy(message: types.Message):
    await message.answer(" отправь нам свой адрес")
    await UserState.adress.set()

@dp.message_handler(state=UserState.adress)
async def fsm(message, state: FSMContext):
    await state.update_data(adress=message.text)
    date = await state.get_data()

    await message.answer(f"доставка будет отправлена на {date['adress']}")







if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
