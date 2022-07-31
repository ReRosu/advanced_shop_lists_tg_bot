from typing import Optional

from pydantic import BaseModel, Field


class ShopListInDb(BaseModel):
    id: int
    shop_list: str
    creator_user_id: int
    name: str
    is_over: bool


class AddShopListInDb(BaseModel):
    shop_list: str
    creator_user_id: int
    name: str


class UpdateShopListInDb(BaseModel):
    shop_list: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    is_over: Optional[bool] = Field(None)
