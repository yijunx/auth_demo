from typing import Dict
from app.schemas import StandardResponse
from pydantic import BaseModel


def create_response(
    response: BaseModel = None,
    success: bool = True,
    message: str = None,
    status: int = 200,
    headers: Dict = None,
):
    resp = StandardResponse(success=success, response=response, message=message)
    return resp.dict(), status, headers
