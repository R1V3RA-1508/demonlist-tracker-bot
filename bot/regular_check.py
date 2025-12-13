import sqlite3
from bot.api import check_lists
from bot.helpers.time_h import current_date

db_obj = sqlite3.connect("db/subs.db")
db = db_obj.cursor()


async def check(bot):
    # checking = await message.reply("⏳️ Проверяю...")
    ids = db.execute("SELECT id FROM users;").fetchone()
    changes = await check_lists()
    # changes.append({"name": "test", "place": 69, "current_place": 67})
    msg = f"<b>Изменения на {current_date()}</b>\n"
    if len(changes) != 0:
        for d in changes:
            msg += f"\
- <b><code>{d.get('name')}</code></b> переместился с <b>{d.get('place')}</b> на <b>{d.get('current_place')}</b> позицию\n\
"
        for id in ids:
            await bot.send_message(text=msg, chat_id=id)
    else:
        # await bot.send_message(text=msg + "Нет изменений", chat_id=2110265968)
        pass
