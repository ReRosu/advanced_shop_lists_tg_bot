from typing import Optional

from sqlalchemy import select, exists

from source.db import tables
from source.db.base import db
from source.models.friends import AddFriendInDb, FriendsInDb


class FriendsRep:
    @staticmethod
    async def add(friendship: AddFriendInDb) -> FriendsInDb:
        q = tables.friends.insert(friendship.dict()).returning(tables.friends)
        res = await db.fetch_one(q)
        return FriendsInDb.parse_obj(res)

    # возвращает список id друзей
    @staticmethod
    async def all_friends_by_id(_id: int) -> list[id]:
        q = tables.friends.select().where(tables.friends.c.user_id == _id)
        res = await db.fetch_all(q)
        result_list = [FriendsInDb.parse_obj(d).friend_id for d in res]
        q = tables.friends.select().where(tables.friends.c.friend_id == _id)
        res = await db.fetch_all(q)
        result_list.extend([FriendsInDb.parse_obj(d).user_id for d in res])
        return result_list

    @staticmethod
    async def exists_friendship(user_id: int, friend_id: int) -> bool:
        q = tables.friends.exists().where(tables.friends.c.user_id == user_id, tables.friends.c.friend_id == friend_id)
        res = await db.fetch_one(q)
        result = [res[0]]
        q = tables.friends.exists().where(tables.friends.c.user_id == friend_id, tables.friends.c.friend_id == user_id)
        res = await db.fetch_one(q)
        result.append(res[0])
        return result[0] is not None or result[1] is not None

    @staticmethod
    async def delete_friendship(user_id: int, friend_id: int) -> bool:
        if await FriendsRep.exists_friendship(user_id, friend_id):
            q = tables.friends.delete().where(
                (tables.friends.c.user_id == user_id and tables.friends.c.friend_id == friend_id) or (
                            tables.friends.c.user_id == friend_id and tables.friends.c.friend_id == user_id))
            res = await db.execute(q)
            return res

