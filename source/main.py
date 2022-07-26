from aiogram.types import BotCommand

from source.bot.bot import executor, dp, bot
from source.bot.handlers import cmds


async def set_commands(*args, **kwargs):
    await dp.bot.set_my_commands([
        BotCommand("start", "Start"),
        BotCommand('comment', 'Comment user'),
        BotCommand("my_comments", "My comments"),
        BotCommand("all_comments", "All comments")
    ])



def main():
    executor.on_startup(set_commands)
    executor.start_polling(reset_webhook=True)


if __name__ == '__main__':
    main()
