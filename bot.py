import os, asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

TOKEN=os.environ["BOT_TOKEN"]
ADMIN_ID=int(os.environ["ADMIN_ID"])
bot=Bot(TOKEN)
dp=Dispatcher()

@dp.message(F.text)
async def t(m:Message):
    await bot.send_message(ADMIN_ID,f"💬 Анонимное сообщение:\n\n{m.text}")
    await m.answer("✅ Отправлено.")

@dp.message(F.photo)
async def p(m:Message):
    await bot.send_photo(ADMIN_ID,m.photo[-1].file_id,caption=m.caption)
    await m.answer("✅ Отправлено.")

@dp.message(F.video)
async def v(m:Message):
    await bot.send_video(ADMIN_ID,m.video.file_id,caption=m.caption)
    await m.answer("✅ Отправлено.")

@dp.message(F.voice)
async def vc(m:Message):
    await bot.send_voice(ADMIN_ID,m.voice.file_id)
    await m.answer("✅ Отправлено.")

@dp.message()
async def other(m:Message):
    await m.answer("Поддерживаются только текст, фото, видео и голосовые.")

async def main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
