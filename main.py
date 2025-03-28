import asyncio
import edge_tts
from aiogram import Bot, Dispatcher
from aiogram.types import Message, FSInputFile, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import tempfile  # Vaqtinchalik fayl yaratish uchun

TOKEN = "7572700059:AAHCU4Kf4RrLIZf7EEnqKh2ZJ1_YjxTOyrY"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Ovoz tanlash uchun klaviatura
voice_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔵 Erkak"), KeyboardButton(text="🔴 Ayol")]
    ],
    resize_keyboard=True
)

user_voices = {}  # Har bir foydalanuvchi uchun ovozni saqlash

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("🎙 Ovoz turini tanlang:", reply_markup=voice_keyboard)

@dp.message()
async def set_voice(message: Message):
    user_id = message.from_user.id

    if message.text == "🔵 Erkak":
        user_voices[user_id] = "uz-UZ-SardorNeural"
        await message.answer("✅ Erkak ovozi tanlandi! Endi matn yuboring.")
    elif message.text == "🔴 Ayol":
        user_voices[user_id] = "uz-UZ-MadinaNeural"
        await message.answer("✅ Ayol ovozi tanlandi! Endi matn yuboring.")
    else:
        if user_id not in user_voices:
            await message.answer("❗️ Iltimos, avval ovoz turini tanlang!", reply_markup=voice_keyboard)
            return

        text = message.text
        if len(text) > 500:
            await message.answer("❌ Matn juda uzun! 500 belgidan kamroq yuboring.")
            return

        # Faylni vaqtinchalik yaratamiz
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_file:
            file_path = temp_file.name  # Fayl nomini olamiz

            tts = edge_tts.Communicate(text, voice=user_voices[user_id])
            await tts.save(file_path)

            # Faylni yuboramiz
            await message.answer_audio(FSInputFile(file_path))

            # Fayl avtomatik ochib ketadi, biz qo‘lda ochirishimiz shart emas

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
