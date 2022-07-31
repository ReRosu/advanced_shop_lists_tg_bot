import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram.utils.executor import Executor

from source.core.settings import load_bot_config

bot_cfg = load_bot_config("bot/bot_config/bot.ini")
bot_token = bot_cfg.tg_bot.token

bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
memory_storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=memory_storage, loop=asyncio.get_event_loop())
executor = Executor(dispatcher=dp, skip_updates=True)
