import asyncio
import aiohttp
from bot.helpers.time_h import time_machine_param


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
