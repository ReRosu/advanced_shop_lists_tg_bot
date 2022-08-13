from typing import Optional
from sqlalchemy import select, exists

from source.db import tables
from source.db.base import db
from source.models.wish import WishInDb, AddWishInDb


class WishesRep:
    @staticmethod
    async def add(wish: AddWishInDb) -> WishInDb:
        q = tables.wishes.insert(wish.dict()).returning(tables.wishes)
        res = await db.fetch_one(q)
        return WishInDb.parse_obj(res)

    @staticmethod
    async def all() -> list[WishInDb]:
        q = tables.wishes.select()
        res = await db.fetch_all(q)
        return [WishInDb.parse_obj(d) for d in res]

    @staticmethod
    async def all_done() -> list[WishInDb]:
        q = tables.wishes.select().where(tables.wishes.c.is_done == True)
        res = await db.fetch_all(q)
        return [WishInDb.parse_obj(d) for d in res]

    @staticmethod
    async def all_not_done() -> list[WishInDb]:
        q = tables.wishes.select().where(tables.wishes.c.is_done == False)
        res = await db.fetch_all(q)
        return [WishInDb.parse_obj(d) for d in res]

    @staticmethod
    async def all_by_user_id(user_id: int) -> list[WishInDb]:
        q = tables.wishes.select().where(tables.wishes.c.user_id == user_id)
        res = await db.fetch_all(q)
        return [WishInDb.parse_obj(d) for d in res]

    @staticmethod
    async def all_done_by_user_id(user_id: int) -> list[WishInDb]:
        q = tables.wishes.select().where(tables.wishes.c.user_id == user_id and tables.wishes.c.is_done == True)
        res = await db.fetch_all(q)
        return [WishInDb.parse_obj(d) for d in res]
