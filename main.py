from aiogram import Bot, Dispatcher , F
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from states import router as state_router
from callbacks import router as callback_router
from connection import *
from keyboards import *
import asyncio
import os





load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()







HELP_TEXT = (
    "📖Командаҳо:\n"
    "/start — оғози бот🚀\n"
    "/help — кумак ❓\n"
    "/add_product➕ — илова кардани маҳсулоти нав\n"
    "/catalog 🛍 — ҳамаи маҳсулот\n"
    "/product 5 🔎 — маълумоти маҳсулот бо ID\n"
    "/my_orders 🧾 — харидҳои ман\n"
    "/sales 5 📊 — чанд дона фурӯхта шуд (танҳо барои соҳиб)\n"
    "/spending 💰 — ман чанд сомонӣ сарф кардам\n"
    "/cancel ❌— қатъ кардани илова кардани маҳсулот"
)





@dp.message(Command("start"))
async def start_bot(message: Message):
    await message.answer(
        f"Салом👋 {message.from_user.full_name}\n"
        f" Хуш омадед ба Mini Shop Bot 🛒\n{HELP_TEXT}",
        reply_markup=main_key
    )





@dp.message(F.text == "❓ Кумак")
@dp.message(Command("help"))
async def help_bot(message: Message):
    await message.answer(HELP_TEXT)


async def main():
    await create_table()
    print("🚀 Bot started")
    dp.include_router(state_router)
    dp.include_router(callback_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
