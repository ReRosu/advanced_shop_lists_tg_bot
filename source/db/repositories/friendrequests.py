from sqlalchemy import select, exists

from source.db import tables
from source.db.base import db
from source.models.friend_request import *


class FriendRequestsRep:
    @staticmethod
    async def add(friend_request: AddFriendRequestInDb) -> FriendRequestInDb:
        q = tables.friend_requests.insert(friend_request.dict()).returning(tables.friend_requests)
        res = await db.fetch_one(q)
        return FriendRequestInDb.parse_obj(res)

    @staticmethod
    async def id_exists(_id: int) -> bool:
        q = select(exists().where(tables.friend_requests.c.id == _id))
        res = await db.fetch_one(q)
        return res[0]

    @staticmethod
    async def all() -> list[FriendRequestInDb]:
        q = tables.friend_requests.select()
        res = await db.fetch_all(q)
        return [FriendRequestInDb.parse_obj(x) for x in res]

    @staticmethod
    async def all_by_user_id(user_id: int) -> list[FriendRequestInDb]:
        q = tables.friend_requests.select().where(tables.friend_requests.c.first_id == user_id
                                                or tables.friend_requests.c.second_id == user_id)
        res = await db.fetch_all(q)
        return [FriendRequestInDb.parse_obj(x) for x in res]

    @staticmethod
    async def delete_by_id(_id) -> bool:
        q = tables.friend_requests.delete().where(tables.friend_requests.c.id == _id)
        res = await db.execute(q)
        return res[0]
    