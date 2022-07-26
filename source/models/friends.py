from typing import Optional

from pydantic import BaseModel, Field


class FriendsInDb(BaseModel):
    user_id: int
    friend_id: int


class AddFriendInDb(BaseModel):
    user_id: int
    friend_id: int
