import asyncio
import json
from datetime import datetime, timedelta
from aiogram import Bot
from pathlib import Path

from utils.wordgen import get_fake_word

SCHEDULE_FILE = Path("data/subscriptions.json")

# user_id: {"interval": int, "next_time": iso8601 str}
subscriptions = {}

# --- Загрузка/сохранение ---

def load_schedule():
    global subscriptions
    if SCHEDULE_FILE.exists():
        try:
            with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
                subscriptions = {
                    int(uid): {
                        "interval": entry["interval"],
                        "next_time": datetime.fromisoformat(entry["next_time"])
                    }
                    for uid, entry in raw.items()
                }
        except Exception as e:
            print(f"Не удалось загрузить подписки: {e}")

def save_schedule():
    raw = {
        str(uid): {
            "interval": data["interval"],
            "next_time": data["next_time"].isoformat()
        }
        for uid, data in subscriptions.items()
    }
    SCHEDULE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
        json.dump(raw, f, indent=2, ensure_ascii=False)

# --- Управление подписками ---

def add_subscription(user_id: int, minutes: int) -> bool:
    try:
        next_time = datetime.now() + timedelta(minutes=minutes)
        subscriptions[user_id] = {
            "interval": minutes,
            "next_time": next_time
        }
        save_schedule()
        return True
    except Exception as e:
        print(f"Ошибка добавления подписки: {e}")
        return False

def remove_subscription(user_id: int):
    if user_id in subscriptions:
        del subscriptions[user_id]
        save_schedule()

# --- Фоновая задача ---

async def run_scheduler(bot: Bot):
    load_schedule()
    while True:
        now = datetime.now()
        for user_id, data in list(subscriptions.items()):
            if now >= data["next_time"]:
                word, definition = get_fake_word()
                try:
                    await bot.send_message(user_id, f"🧠 Новое слово: *{word}*\nЗначение: _{definition}_", parse_mode="Markdown")
                except Exception as e:
                    print(f"Ошибка при отправке {user_id}: {e}")
                # Обновляем время
                data["next_time"] = now + timedelta(minutes=data["interval"])
                save_schedule()
        await asyncio.sleep(60)
