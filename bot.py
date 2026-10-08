import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from google import genai

# --- SOZLAMALAR ---
TELEGRAM_BOT_TOKEN = "8611513099:AAGj7gJzQbp_GVgAZmZMoX59M24ahNs2zZ8"
GEMINI_API_KEY = "AQ.Ab8RN6Kgzi-A-a57AYjYwDDaFpXhyOVCHT4rkWQDgceVAMFtcQ"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = (
    "Siz Telegram profili egasisiz. Xuddi o'zingiz Telegramda do'stlaringizga yozayotgandek "
    "juda qisqa, samimiy, oddiy odamdek javob bering. "
    "HECH QACHON 'Men AI'man', 'Qanday yordam beray?' kabi rasmiy iboralarni ishlatmang. "
    "Javoblaringiz 1-2 ta qisqa jumladan oshmasin."
)

MODEL_NAME = "gemini-3.8-flash"

GENERATION_CONFIG = {
    "system_instruction": SYSTEM_INSTRUCTION,
    "temperature": 0.7,
    "max_output_tokens": 150
}

@dp.business_message()
async def handle_business(message: Message):
    text_content = message.text or message.caption
    if not text_content:
        return

    try:
        response = gemini_client.models.generate_content(
            model=MODEL_NAME,
            contents=text_content,
            config=GENERATION_CONFIG
        )
        if response.text:
            await bot.send_message(
                chat_id=message.chat.id,
                text=response.text,
                business_connection_id=message.business_connection_id
            )
    except Exception as e:
        print(f"Xatolik: {e}")

@dp.message()
async def handle_direct(message: Message):
    text_content = message.text or message.caption
    if not text_content:
        return

    try:
        response = gemini_client.models.generate_content(
            model=MODEL_NAME,
            contents=text_content,
            config=GENERATION_CONFIG
        )
        if response.text:
            await message.answer(response.text)
    except Exception as e:
        print(f"Xatolik: {e}")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(
        bot, 
        allowed_updates=["message", "business_message", "business_connection"]
    )

if __name__ == "__main__":
    asyncio.run(main())
