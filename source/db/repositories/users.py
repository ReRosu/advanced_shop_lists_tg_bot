from typing import Optional
from sqlalchemy import select, exists

from source.db import tables
from source.db.base import db
from source.models.user import UserInDb, AddUserInDb, UpdateUserInDb


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

    @staticmethod
    async def update_by_id(_id: int, update_user: UpdateUserInDb) -> Optional[UserInDb]:
        data_update = update_user.dict(exclude_none=True)
        if not data_update:
            raise Exception('no data to update')
        if not await UsersRep.id_exists(_id):
            raise Exception('no user with this id')

        q = tables.users.update().values(data_update).where(tables.users.c.id==_id).returning(tables.users)
        res = await db.fetch_one(q)
        return UserInDb.parse_obj(res) if res else None



async def test():
    await db.connect()
    t = await UsersRep.all()
    print(t)
    await db.disconnect()
