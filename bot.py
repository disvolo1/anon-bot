import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = os.getenv("BOT_TOKEN")

# Пример:
# ADMIN_IDS=111111111,222222222
ADMIN_IDS = [
    int(admin_id.strip())
    for admin_id in os.getenv("ADMIN_IDS").split(",")
]

bot = Bot(TOKEN)
dp = Dispatcher()


# ---------------- START ----------------

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        """Привет! 👋

Это анонимный бот
«Подслушано @pingtablet»

Присылай сюда слушок 😇
Можно текст, фото, видео или голосовое.

Твой профиль никто не увидит, даже мы.

Публикация анонимно:
@pingtabletpeople"""
    )


# ---------------- TEXT ----------------

@dp.message(F.text)
async def text_handler(message: Message):
    for admin in ADMIN_IDS:
        await bot.send_message(
            admin,
            f"💬 Анонимное сообщение:\n\n{message.text}"
        )

    await message.answer("✅ Сообщение отправлено!")


# ---------------- PHOTO ----------------

@dp.message(F.photo)
async def photo_handler(message: Message):
    for admin in ADMIN_IDS:
        await bot.send_photo(
            admin,
            message.photo[-1].file_id,
            caption=message.caption or "📷 Анонимное фото"
        )

    await message.answer("✅ Фото отправлено!")


# ---------------- VIDEO ----------------

@dp.message(F.video)
async def video_handler(message: Message):
    for admin in ADMIN_IDS:
        await bot.send_video(
            admin,
            message.video.file_id,
            caption=message.caption or "🎥 Анонимное видео"
        )

    await message.answer("✅ Видео отправлено!")


# ---------------- VOICE ----------------

@dp.message(F.voice)
async def voice_handler(message: Message):
    for admin in ADMIN_IDS:
        await bot.send_voice(
            admin,
            message.voice.file_id
        )

    await message.answer("✅ Голосовое отправлено!")


# ---------------- OTHER ----------------

@dp.message()
async def unsupported(message: Message):
    await message.answer(
        "Можно отправить только:\n\n"
        "• текст\n"
        "• фото\n"
        "• видео\n"
        "• голосовое сообщение"
    )


# ---------------- MAIN ----------------

async def main():
    # Удаляем webhook, если он установлен
    await bot.delete_webhook(drop_pending_updates=True)

    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
