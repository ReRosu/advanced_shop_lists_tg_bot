from typing import Optional

from pydantic import BaseModel, Field


class ShopListToUserInDb(BaseModel):
    shop_list_id: int
    user_id: int


class AddShopListToUserInDb(BaseModel):
    shop_list_id: int
    user_id: int