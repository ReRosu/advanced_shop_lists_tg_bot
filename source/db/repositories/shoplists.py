from typing import Optional
from sqlalchemy import select, exists

from source.db import tables
from source.db.base import db
from source.Models.shoplist import ShopListInDb, AddShopListInDb, UpdateShopListInDb


class ShopListsRep:
    @staticmethod
    async def add(shop_list: AddShopListInDb) -> ShopListInDb:
        q = tables.shop_lists.insert(shop_list.dict()).returning(tables.shop_lists)
        res = await db.fetch_one(q)
        return ShopListInDb.parse_obj(res)

    @staticmethod
    async def id_exists(_id: int) -> bool:
        q = tables.shop_lists.exists().where(tables.shop_lists.c.id == _id)
        res = await db.fetch_one(q)
        return res[0]

    @staticmethod
    async def all() -> list[ShopListInDb]:
        q = tables.shop_lists.select()
        res = await db.fetch_all(q)
        return [ShopListInDb.parse_obj(d) for d in res]

    @staticmethod
    async def all_by_user_id(user_id: int) -> list[ShopListInDb]:
        q = tables.shop_lists.select().where(tables.shop_lists.c.creator_user_id == user_id)
        res = await db.fetch_all(q)
        return [ShopListInDb.parse_obj(d) for d in res]

    @staticmethod
    async def by_id(_id: int) -> Optional[ShopListInDb]:
        q = tables.shop_lists.select().where(tables.shop_lists.c.id == _id)
        res = await db.fetch_one(q)
        return ShopListInDb.parse_obj(res)

    @staticmethod
    async def update_by_id(_id: int, update_shop_list: UpdateShopListInDb) -> ShopListInDb:
        data_update = update_shop_list.dict(exclude_none = True)
        if not data_update:
            raise Exception('no data to update')
        if not ShopListsRep.id_exists(_id):
            raise Exception('no shop_list with this id')
        q = tables.shop_lists.update().values(data_update).where(tables.shop_lists.c.id == _id).returning(tables.shop_lists)
        res = await db.fetch_one(q)
        return ShopListInDb.parse_obj(res) if res else None

    @staticmethod
    async def delete_by_id(_id: int) -> bool:
        q = tables.shop_lists.delete().where(tables.shop_lists.c.id == _id)
        res = await db.execute(q)
        return res

    @staticmethod
    async def delete_user_data_from_id(_id):
        tmp = await ShopListsRep.by_id(_id)
        await ShopListsRep.delete_by_id(_id)
        await ShopListsRep.add(AddShopListInDb(shop_list=tmp.shop_list, creator_user_id=None, name='ToStatistics', users_with_permission=None))


