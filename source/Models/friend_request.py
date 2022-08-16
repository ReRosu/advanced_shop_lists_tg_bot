from pydantic import BaseModel


class FriendRequestInDb(BaseModel):
    id: int
    first_id: int
    second_id: int


class AddFriendRequestInDb(BaseModel):
    first_id: int
    second_id: int
