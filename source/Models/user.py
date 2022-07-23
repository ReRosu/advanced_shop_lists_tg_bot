from typing import Optional

from pydantic import BaseModel, Field


class UserInDb(BaseModel):
    id: int


class AddUserInDb(BaseModel):
    id: int

