import aiohttp
import asyncio
import logging
import sys
from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

load_dotenv()
TOKEN = os.getenv("token")

dp = Dispatcher()


def split(text: str, max_length: int = 4096) -> list[str]:
    if len(text) <= max_length:
        return [text]

    parts = []
    start = 0

    while start < len(text):
        end = start + max_length

        if end >= len(text):
            parts.append(text[start:])
            break

        last_close_tag = text.rfind("</code>", start, end)

        if last_close_tag != -1:
            end = last_close_tag + len("</code>")
        else:
            last_open_tag = text.rfind("<code>", start, end)

            if last_open_tag != -1:
                next_close_tag = text.find("</code>", last_open_tag)

                if next_close_tag != -1 and next_close_tag < len(text):
                    end = next_close_tag + len("</code>")
                else:
                    end = last_open_tag
            else:
                last_semicolon = text.rfind(";", start, end)
                if last_semicolon != -1:
                    end = last_semicolon + 1

        parts.append(text[start:end])
        start = end

    return parts


# https://api.demonlist.org/levels/classic/time_machine?timestamp=2025-12-10T07:40:00.000Z


async def get_list(limit=50):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.demonlist.org/levels/classic?search=&levels_type=all&offset=0&limit={limit}"
        ) as r:
            demons = await r.json()
    temp = []
    for d in demons.get("data"):
        temp.append(
            f"{d.get('place')}: <code>{d.get('name')}</code> от <code>{d.get('creator')}</code>. Верифер: <code>{d.get('verifier')}</code>. ID: <code>{d.get('level_id')}</code>"
        )
    return "\n".join(temp)


async def get_demon(place):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.demonlist.org/levels/classic?place={place}"
        ) as r:
            demon = await r.json()
    data = demon["data"][0]
    temp = []
    temp.append(
        [
            f"📈 Позиция: {place}",
            f"📝 Название: <code>{data.get('name')}</code>",
            f"🛠️ Креатор: <code>{data.get('creator')}</code>",
            f"⚔️ Верифер: <code>{data.get('verifier')}</code>",
            f"🪧 Описание: <blockquote>{data.get('description')}</blockquote>",
            f"🪪 Айди уровня: <code>{data.get('level_id')}</code>",
        ]
    )
    return "\n".join(temp[0])


@dp.message(CommandStart())
async def start(message):
    await message.reply(
        "👋 Привет! Я отслеживаю Global Demonlist - изменения в топе, а еще могу дать список демонов и инфу о демоне прямо в Телеграме!\n\nУзнать команды: /help"
    )


@dp.message(Command("list"))
async def list_cmd(message):
    if message.text.replace("/list", "") != "":
        try:
            limit = int(message.text.replace("/list ", ""))
        except ValueError:
            await message.reply("⛔️ Не число!")
            return False
    else:
        limit = 10
    demon_list = await get_list(limit)
    lst = split(demon_list)
    for d in lst:
        await message.reply(d)


@dp.message(Command("demon"))
async def demon_cmd(message):
    if message.text.replace("/demon", "") != "":
        try:
            place = int(message.text.replace("/demon ", ""))
        except ValueError:
            await message.reply("⛔️ Не число!")
            return False
        await message.reply(await get_demon(place))
    else:
        await message.reply("⛔️ Введите позицию!")


@dp.message(Command("help"))
async def help_cmd(message):
    await message.answer("""
/help - вывести это сообщение\n\
/list [лимит] - вывести топ-[лимит] демонов. По умолчанию лимит 10.\n\
/demon [позиция] - получить информацию о демоне с позиции\
""")


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
