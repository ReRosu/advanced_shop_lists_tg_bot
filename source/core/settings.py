import configparser
from dataclasses import dataclass

TG_TOKEN = "5422195989:AAFgwEpdmogZ2iyW1XqovAu5ly7rAkp1YzQ"
db_url = 'postgresql+psycopg2://postgres:minesv123@localhost/postgres'

@dataclass()
class TgBot:
    token: str
    admin_id: int


@dataclass()
class Config:
    tg_bot: TgBot


@dataclass()
class Db:
    db_url: str


def load_bot_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            admin_id=int(tg_bot["admin_id"])
        )
    )


def load_db_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    db = config["db"]

    return Db(
        db_url=db["db_url"]
    )
