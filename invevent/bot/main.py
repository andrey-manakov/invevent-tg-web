import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from invevent.models import User
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your.domain/webapp")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    session = SessionLocal()
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user:
        user = User(telegram_id=message.from_user.id, username=message.from_user.username)
        session.add(user)
        session.commit()
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Open Event Map", web_app=WebAppInfo(url=WEBAPP_URL))]
    ], resize_keyboard=True)
    await message.answer("Welcome to Invevent! Use the button below to see and create events.", reply_markup=kb)
    session.close()

# More handlers for /addevent, /myevents, /friends, etc. can be added here

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
