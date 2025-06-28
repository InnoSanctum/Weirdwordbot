from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from utils.wordgen import get_fake_word

from scheduler import add_subscription, remove_subscription

router = Router()

@router.message(Command("ping"))
async def send_fake_word(message: Message):
    word, definition = get_fake_word()
    await message.answer(f"🧠 Новое слово: *{word}*\nЗначение: _{definition}_", parse_mode="Markdown")

@router.message(Command("частота"))
async def set_frequency(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("Пожалуйста, укажи в команде число, например: /частота 3")
        return 
    try:
        minutes = int(command.args)
        
        if minutes < 1 or minutes > 1440:
            raise ValueError("Out of range")
    except (ValueError, TypeError):
        await message.answer("Пожалуйста, укажи число от 1 до 1440 (минут между сообщениями).")
        return
    
    if not (add_subscription(message.from_user.id, minutes)): 
        await message.answer("Какая-то ошибка.")
        return
    await message.answer(f"Буду присылать тебе слова каждые {minutes} минут.\nДля прекращения пришли /стоп")

@router.message(Command("стоп"))
async def stop_auto(message: Message):
    remove_subscription(message.from_user.id)
    await message.answer("Окей, больше не буду писать сам.")
