import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

TOKEN = os.getenv("BOT_TOKEN")
CHAT = os.getenv("CHAT_ID")

if not TOKEN:
    print("укажи BOT_TOKEN в .env")
    exit()

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("Привет! Напиши сюда свою заявку текстом или фото, и я передам её дальше.")

@dp.message(F.text | F.photo)
async def заявку(m: types.Message):
    name = m.from_user.full_name
    user = f"@{m.from_user.username}" if m.from_user.username else ""
    head = f"Заявка от {name} {user} (id {m.from_user.id}):"

    try:
        if m.photo:
            cap = m.caption or ""
            text = f"{head}\n{cap}" if cap else head
            await bot.send_photo(CHAT, m.photo[-1].file_id, caption=text)
        else:
            await bot.send_message(CHAT, f"{head}\n{m.text}")
        await m.answer("Заявка принята, спасибо!")
    except Exception as e:
        print(f"не смог переслать: {e}")
        await m.answer("Заявка принята, но не смог переслать админу")

@dp.message()
async def other(m: types.Message):
    await m.answer("принимаю только текст и фото")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
