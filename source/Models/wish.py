from pydantic import BaseModel


class WishInDb(BaseModel):
    id: int
    message: str
    user_id: int
    is_done: bool


class AddWishInDb(BaseModel):
    message: str
    user_id: int
