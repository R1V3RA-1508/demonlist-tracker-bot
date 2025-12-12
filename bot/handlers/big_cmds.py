from aiogram import Router
from aiogram.filters import Command

from bot.helpers.time_h import current_date
from bot.api import get_list, get_demon, check_lists
from bot.helpers.split import split

dp = Router()


@dp.message(Command("list"))
async def list_cmd(message, bot):
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
async def prev_cmd(message, bot):
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
async def demon_cmd(message, bot):
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
