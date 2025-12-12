import asyncio

from aiogram import Router
from aiogram.filters import CommandStart, Command

dp = Router()


@dp.message(CommandStart())
async def start(message):
    await message.reply(
        "👋 Привет! Я отслеживаю Global Demonlist - изменения в топе, а еще могу дать список демонов и инфу о демоне прямо в Телеграме!\n\nУзнать команды: /help"
    )


@dp.message(Command("help"))
async def help_cmd(message):
    await message.answer("""
/help - вывести это сообщение\n\
/list [лимит] - вывести топ-[лимит] демонов. По умолчанию лимит 10.\n\
/demon [позиция] - получить информацию о демоне с позиции\n\
/changes - узнать, позиции каких демонов изменились\
""")
