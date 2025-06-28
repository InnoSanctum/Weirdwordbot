from aiogram import Dispatcher
from handlers import ping

def setup_bot(dp: Dispatcher):
    dp.include_router(ping.router)
