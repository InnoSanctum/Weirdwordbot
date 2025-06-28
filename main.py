import asyncio
from aiogram import Bot, Dispatcher
from bot import setup_bot

from config import BOT_TOKEN
from scheduler import run_scheduler
from utils.wordgen import build_vocab

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    setup_bot(dp)  # Регистрируем хендлеры
    build_vocab()
     # Запускаем планировщик параллельно
    scheduler_task = asyncio.create_task(run_scheduler(bot))

    await dp.start_polling(bot)
    scheduler_task.cancel()
   

if __name__ == "__main__":
    
    asyncio.run(main())
