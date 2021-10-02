from pydantic import BaseModel
from typing import Any, List, Optional


class Role(BaseModel):
    name: str


class User(BaseModel):
    id: str
    name: str
    email: str
    roles: List[Role]


class StandardResponse(BaseModel):
    success: bool
    response: Any
    message: Optional[str]


class Resource(BaseModel):
    id: str
    created_by: str
    name: str
