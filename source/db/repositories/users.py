from typing import Optional
from sqlalchemy import select, exists

from source.db import tables
from source.db.base import db
from source.Models.user import UserInDb, AddUserInDb


class UsersRep:
    @staticmethod
    async def add(add_user: AddUserInDb) -> UserInDb:
        q = tables.users.insert(add_user.dict()).returning(tables.users)
        res = await db.fetch_one(q)
        return UserInDb.parse_obj(res)

    @staticmethod
    async def id_exists(_id: int) -> bool:
        q = select(exists().where(tables.users.c.id == _id))
        res = await db.fetch_one(q)
        return res[0]

    @staticmethod
    async def all() -> list[UserInDb]:
        q = tables.users.select()
        res = await db.fetch_all(q)
        return [UserInDb.parse_obj(d) for d in res]

    @staticmethod
    async def by_id(_id: int) -> Optional[UserInDb]:
        q = tables.users.select().where(tables.users.c.id == _id)
        res = await db.fetch_one(q)
        return UserInDb.parse_obj(res) if res else None

    @staticmethod
    async def delete_by_id(_id: int) -> bool:
        q = tables.users.delete().where(tables.users.c.id == _id)
        res = await db.execute(q)
        return res[0]


async def test():
    await db.connect()
    t = await UsersRep.all()
    print(t)
    await db.disconnect()
