
import os
from dotenv import load_dotenv

from telethon import TelegramClient, events
from telethon.sessions import StringSession
import openai
import asyncio


# 1. .env faylni yuklaymiz
load_dotenv()

# 2. OpenAI kalitini .env fayldan olamiz
openai.api_key = os.getenv("OPENAI_API_KEY")

# 3. Telegram uchun API ID, HASH va StringSession .env dan olinadi
api_id = 26968121  # .env faylidan API_ID olish
api_hash = "bee8f7a35a42028df27198097365364c"  # .env faylidan API_HASH olish
session_string = "1ApWapzMBuxIw4tfNJV8YrSWkIubliGjWYASHYmpuJgYwIzjthe-S0KqyovVm5-sFJRksnNEAw3k2xz3iOc72AbI4TuPDYdjy-i1yEVcXMXq4llDlDu4UprRd-ADkLBTJVQKegDaZQi3ZnCZa6WLg3NWmbsdYGcZ5WcrTmb2s1qmYZNkVaxuCdqdblICvnCqvcIzl_ZFJy8BGkfRszujVlBBbWWZcw6LE86VYAESnTxQbVlt6yNQe5-vTSid-H0T3f5y-IoVx2ovl9FCcHdLsZmkv2qUK-p2mWtDyt0WUezJUF3LFqgLjCjQf5Od6F1dL1d-RdILQd1ByWW3sAxP-kRMWN7oluqM="  # .env faylidan SESSION_STRING olish

# 4. Telegram klientini yaratamiz
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# 5. ChatGPT'dan javob olish funksiyasi
async def get_gpt_response(message):
    try:
        # Yangi OpenAI API formatiga moslashtirilgan kod
        response = openai.completions.create(
            model="gpt-3.5-turbo",  # Yoki yangi modelni ishlatishingiz mumkin
            messages=[{
                "role": "system", 
                "content": "Sen Husanjon Musayevsan. Oddiy, samimiy, hazilkash ohangda gapirasan."
            },
            {
                "role": "user", 
                "content": message
            }],
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Xatolik: {e}"

# 6. Telegramda yangi xabar kelganda javob beruvchi funksiyani yozamiz
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    if event.is_private:
        user_message = event.raw_text
        await asyncio.sleep(2)
        reply = await get_gpt_response(user_message)
        await event.reply(reply)

# 7. Botni ishga tushiramiz
async def main():
    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())
