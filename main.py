# import aiohttp
import asyncio
import logging
import sys
from dotenv import load_dotenv
import os
from pathlib import Path

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


async def main():
    dp.include_router(dp_big)
    dp.include_router(dp_small)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
