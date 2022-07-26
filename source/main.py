from aiogram.types import BotCommand

from source.bot.bot import executor, dp


def main():
    executor.start_polling(reset_webhook=True, fast=True)


if __name__ == '__main__':
    main()