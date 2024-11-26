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
button_inline = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
button_inline_2 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
ikb.add(button_inline, button_inline_2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Привет! Я бот, помогающий следить за здоровьем. Выберите действие:", reply_markup=kb)


@dp.message_handler(text="Рассчитать")
async def main_menu(message: types.Message):
    """
    Обработчик кнопки 'Рассчитать' из Reply клавиатуры.
    """
    await message.answer("Выберите опцию:", reply_markup=ikb)


@dp.callback_query_handler(text="calories")
async def set_age(call: types.CallbackQuery):
    """
    Начало машины состояний, обработка кнопки 'Рассчитать норму калорий'.
    """
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()
@dp.callback_query_handler(text="formulas")
async def formulas(call: types.CallbackQuery):
    formulas_text = (
        "Формула для мужчин: 10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (г) + 5\n"
        "Формула для женщин: 10 × вес (кг) + 6.25 × рост (см) − 5 × возраст (г) − 161"
    )
    await call.message.answer(formulas_text)
    await call.answer()

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



@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def all_messages(message: types.Message):
    """
    Обработчик для всех остальных сообщений.
    """
    await message.answer("Я вас не понимаю. Пожалуйста, выберите действие с помощью кнопок.", reply_markup=kb)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)