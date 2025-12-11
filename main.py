import aiohttp
import asyncio
import logging
import sys
from dotenv import load_dotenv
import os
from time_h import time_machine_param, current_date

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command

load_dotenv()
TOKEN = os.getenv("token")

dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


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


# https://api.demonlist.org/levels/classic/time_machine?timestamp={hour_ago()}


async def get_prev_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.demonlist.org/levels/classic/time_machine?timestamp={time_machine_param()}"
        ) as r:
            prev_list = await r.json()
        return prev_list["data"]


async def check_lists():
    prev_list = await get_prev_list()
    lst = []
    for d in prev_list:
        if d.get("place") == d.get("current_place"):
            pass
        else:
            lst.append(d)
    return lst


async def get_list(limit=50):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.demonlist.org/levels/classic?search=&levels_type=all&offset=0&limit={limit}"
        ) as r:
            demons = await r.json()
    temp = []
    for d in demons.get("data"):
        temp.append(
            f"<b>{d.get('place')}:</b> <code><b>{d.get('name')}</b></code> от <code>{d.get('creator')}</code>. Верифер: <code>{d.get('verifier')}</code>. ID: <code>{d.get('level_id')}</code>"
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
    checking = await message.reply("⏳️ Получаю...")
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
    await bot.delete_message(chat_id=message.chat.id, message_id=checking.message_id)
    for d in lst:
        await message.reply(d)


@dp.message(Command("changes"))
async def prev_cmd(message):
    checking = await message.reply("⏳️ Проверяю...")
    changes = await check_lists()
    msg = f"<b>Изменения на {current_date()}</b>\n"
    if len(changes) != 0:
        for d in changes:
            msg += f"\
- <b><code>{d.get('name')}</code></b> переместился с <b>{d.get('place')}</b> на <b>{d.get('current_place')}</b> позицию\n\
"
        await bot.edit_message_text(
            text=msg, chat_id=message.chat.id, message_id=checking.message_id
        )
    else:
        await bot.edit_message_text(
            text="🚫 Нет изменений",
            chat_id=message.chat.id,
            message_id=checking.message_id,
        )


@dp.message(Command("demon"))
async def demon_cmd(message):
    if message.text.replace("/demon", "") != "":
        try:
            place = int(message.text.replace("/demon ", ""))
        except ValueError:
            await message.reply("⛔️ Не число!")
            return False
        checking = await message.reply("⏳️ Получаю...")
        await bot.edit_message_text(
            text=await get_demon(place),
            chat_id=message.chat.id,
            message_id=checking.message_id,
        )
    else:
        await message.reply("⛔️ Введите позицию!")


@dp.message(Command("status"))
async def status_cmd(message):
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.demonlist.org/levels/classic?place=1"
        ) as r:
            api_code = r.status
            if api_code > 200:
                api_status = "Недоступен"


@dp.message(Command("help"))
async def help_cmd(message):
    await message.answer("""
/help - вывести это сообщение\n\
/list [лимит] - вывести топ-[лимит] демонов. По умолчанию лимит 10.\n\
/demon [позиция] - получить информацию о демоне с позиции\n\
/changes - узнать, позиции каких демонов изменились\
""")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
