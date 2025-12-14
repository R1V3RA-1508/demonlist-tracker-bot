import asyncio
import sqlite3
import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command

from bot.helpers.split import split

dp = Router()
db_obj = sqlite3.connect("db/subs.db")
db = db_obj.cursor()

creator_id = 2110265968


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


@dp.message(Command("sub"))
async def sub_cmd(message):
    try:
        if (
            db.execute(f"SELECT id FROM users WHERE id = {message.chat.id}").fetchone()
            is None
        ):
            db.execute(f"INSERT INTO users (id) VALUES ({message.chat.id})")
            await message.reply("✅ Вы подписались на ежедневную рассылку изменений")
            logging.info(f"New record in db: {message.chat.id}")
            db_obj.commit()
        else:
            await message.reply("🚫 Вы уже подписаны!")
    except Exception as e:
        logging.error(e)
        await message.reply("⛔️ Ошибка: не удалось подписаться на рассылку")


@dp.message(Command("unsub"))
async def unsub_cmd(message):
    try:
        if (
            db.execute(f"SELECT id FROM users WHERE id = {message.chat.id}").fetchone()
            is not None
        ):
            db.execute(f"DELETE FROM users WHERE id = ({message.chat.id})")
            await message.reply("✅ Вы отписались от ежедневной рассылки изменений")
            logging.info(f"Deleted record from db: {message.chat.id}")
            db_obj.commit()
        else:
            await message.reply("🚫 Вы не подписаны!")
    except Exception as e:
        logging.error(e)
        await message.reply("⛔️ Ошибка: не удалось отписаться от рассылки")


@dp.message(Command("db"))
async def db_cmd(message):
    if message.chat.id == creator_id:
        database = db.execute("SELECT id FROM users;").fetchone()
        split_db = split(str(database))
        for i in split_db:
            await message.reply(i)
