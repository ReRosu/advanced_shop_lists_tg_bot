from pydantic import BaseModel


class FriendsInDb(BaseModel):
    user_id: int
    friend_id: int


class AddFriendInDb(BaseModel):
    user_id: int
    friend_id: int
