from sqlalchemy import select, exists

from source.db import tables
from source.db.base import db
from source.models.shoplisttouser import ShopListToUserInDb, AddShopListToUserInDb


class ShopListsToUsersRep:
    @staticmethod
    async def add(sl_to_user_relationship: AddShopListToUserInDb):
        q = tables.shop_lists_to_users.insert(sl_to_user_relationship.dict()).returning(tables.shop_lists_to_users)
        res = await db.fetch_one(q)
        return ShopListToUserInDb.parse_obj(res)

    @staticmethod
    async def all_by_shop_list_id(sl_id: int):
        q = tables.shop_lists_to_users.select().where(tables.shop_lists_to_users.c.shop_list_id == sl_id)
        res = await db.fetch_all(q)
        return [ShopListToUserInDb.parse_obj(d).user_id for d in res]

    @staticmethod
    async def all_by_user_id(u_id: int):
        q = tables.shop_lists_to_users.select().where(tables.shop_lists_to_users.c.user_id == u_id)
        res = await db.fetch_all(q)
        return [ShopListToUserInDb.parse_obj(d).shop_list_id for d in res]

    @staticmethod
    async def delete_user_from_shop_list(u_id: int, sl_id: int):
        q = tables.shop_lists_to_users.delete().where(tables.shop_lists_to_users.c.shop_list_id == sl_id,
                                                      tables.shop_lists_to_users.c.user_id == u_id)
        res = await db.execute(q)
        return res
