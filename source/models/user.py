from typing import Optional

from pydantic import BaseModel, Field


class UserInDb(BaseModel):
    id: int
    user_name: Optional[str]


class AddUserInDb(BaseModel):
    id: int
    user_name: str


class UpdateUserInDb(BaseModel):
    user_name: Optional[str] = Field(None)

