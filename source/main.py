from aiogram.types import BotCommand
import asyncio
from source.bot.bot import executor, dp
import bot.handlers.cmds
from source.db import base, tables


async def set_commands(*args, **kwargs):
    await dp.bot.set_my_commands([
        BotCommand("start", "Start")
    ])


def main():
    executor.on_startup(set_commands)
    executor.loop.run_until_complete(base.db.connect())
    executor.start_polling(reset_webhook=True)
    executor.loop.run_until_complete(base.db.disconnect())


if __name__ == '__main__':
    main()