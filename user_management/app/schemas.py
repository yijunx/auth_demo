from pydantic import BaseModel
from typing import Any, List, Optional


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
    password: bytes


class StandardResponse(BaseModel):
    success: bool
    response: Any
    message: Optional[str]


class Token(BaseModel):
    access_token: str
