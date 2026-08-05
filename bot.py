import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(TOKEN)
dp = Dispatcher()


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


@dp.message(F.text)
async def text_handler(message: Message):
    await bot.send_message(
        ADMIN_ID,
        f"💬 Анонимное сообщение:\n\n{message.text}"
    )
    await message.answer("✅ Отправлено!")


@dp.message(F.photo)
async def photo_handler(message: Message):
    await bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=message.caption or ""
    )
    await message.answer("✅ Фото отправлено!")


@dp.message(F.video)
async def video_handler(message: Message):
    await bot.send_video(
        ADMIN_ID,
        message.video.file_id,
        caption=message.caption or ""
    )
    await message.answer("✅ Видео отправлено!")


@dp.message(F.voice)
async def voice_handler(message: Message):
    await bot.send_voice(
        ADMIN_ID,
        message.voice.file_id
    )
    await message.answer("✅ Голосовое отправлено!")


@dp.message()
async def unsupported(message: Message):
    await message.answer(
        "Поддерживаются только:\n"
        "• текст\n"
        "• фото\n"
        "• видео\n"
        "• голосовые сообщения"
    )


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
