import os
from pathlib import Path

os.mkdir(f"{str(Path(__file__).parent)}/db")
import asyncio
import logging
import sys
from dotenv import load_dotenv
import sqlite3
from bot.regular_check import check

sys.path.append(str(Path(__file__).parent))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.handlers.big_cmds import dp as dp_big
from bot.handlers.small_cmds import dp as dp_small

load_dotenv()
TOKEN = os.getenv("token")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def init_db():
    db = sqlite3.connect("db/subs.db").cursor()
    logging.info("Connected to subs.db")
    try:
        db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY);")
        logging.info('Table "users" created')
    except sqlite3.OperationalError:
        logging.info('Table "users" already exists')
        if db.execute("SELECT id FROM users;").fetchone() is not None:
            logging.info(
                f"Number of IDs in db: {len(db.execute('SELECT id FROM users;').fetchone())}"
            )
        else:
            logging.info("db is empty")


async def periodic_check(bot):
    while True:
        try:
            await check(bot)
        except Exception as e:
            logging.error(e)
        await asyncio.sleep(86400)


async def main():
    init_db()
    # dp.include_router(dp_big)
    # dp.include_router(dp_small)
    asyncio.create_task(periodic_check(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
