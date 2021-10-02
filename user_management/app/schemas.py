from pydantic import BaseModel
from typing import List


class UserLogin(BaseModel):
    email: str
    password: str


class Role(BaseModel):
    name: str


class User(BaseModel):
    id: str
    name: str
    email: str
    roles: List[Role]


class UserWithPassword(User):
    password: str
