import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import logging
from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


# Состояния
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL, 
        age INTEGER NOT NULL, 
        grade TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(f"Привет! Как тебя зовут?")
    await state.set_state(Form.name)


@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"Сколько тебе лет?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(f"В каком классе ты учишься?")
    await state.set_state(Form.grade)


@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
                (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    # Вывод введенных данных пользователю
    await message.answer(
        f"Спасибо! Твои данные сохранены.\n\n"
        f"Имя: {user_data['name']}\n"
        f"Возраст: {user_data['age']}\n"
        f"Класс: {user_data['grade']}"
    )
    await state.clear()


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
