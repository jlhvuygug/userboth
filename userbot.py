import os
from dotenv import load_dotenv  # .env fayldan ma'lumot yuklash uchun

from telethon import TelegramClient, events
import openai
import asyncio

# 1. .env faylni yuklaymiz
load_dotenv()

# 2. OpenAI kalitini .env fayldan olamiz
openai.api_key = os.getenv("OPENAI_API_KEY")

# 3. Telegram uchun API ID va HASH to'g'ridan-to'g'ri yozilgan (xavfsiz bo'lishi uchun aslida .env faylga o‘tkazish kerak)
api_id = 26968121
api_hash = "bee8f7a35a42028df27198097365364c"

# 4. Telegram sessiya fayl nomi
client = TelegramClient('husanjon_session', api_id, api_hash)

# 5. ChatGPT'dan javob olish funksiyasi
async def get_gpt_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # yoki 'gpt-4' mavjud bo‘lsa
            messages=[
                {"role": "system", "content": "Sen Husanjon Musayevsan. Oddiy, samimiy, hazilkash ohangda gapirasan."},
                {"role": "user", "content": message}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Xatolik: {e}"

# 6. Telegramda yangi xabar kelganda javob beruvchi funksiyani yozamiz
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:  # Faqat shaxsiy chatlarga javob beradi
        user_message = event.raw_text
        await asyncio.sleep(2)  # Javob tabii ko‘rinsin deb 2 soniya kutish
        reply = await get_gpt_response(user_message)
        await event.reply(reply)

# 7. Botni ishga tushiramiz
client.start()
client.run_until_disconnected()
